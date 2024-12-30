# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=missing-module-docstring
# pylint: disable=broad-exception-caught

from datetime import date, datetime, timedelta
import json
import math
import os
import sys

from typing import List, Tuple, TypedDict

from google.api_core import exceptions
from google.cloud import logging_v2, storage

# Logging limits (https://cloud.google.com/logging/quotas#api-limits)
_LOGS_MAX_SIZE_BYTES = 9 * 1024 * 1024  # < 10MB

# Read Cloud Run environment variables
TASK_INDEX = int(os.getenv("CLOUD_RUN_TASK_INDEX", "0"))
TASK_COUNT = int(os.getenv("CLOUD_RUN_TASK_COUNT", "1"))


def getenv_date(name: str) -> date:
    """Reads environment variable and converts it to 'datetime.date'"""
    date_str = os.getenv(name)
    if not date_str:
        return None
    return datetime.strptime(date_str, "%m/%d/%Y").date()


# Read import parameters' environment variables
START_DATE = getenv_date("START_DATE")
END_DATE = getenv_date("END_DATE")
LOG_ID = os.getenv("LOG_ID")
BUCKET_NAME = os.getenv("STORAGE_BUCKET_NAME")
PROJECT_ID = os.getenv("PROJECT_ID")


def eprint(*objects: str, **kwargs: TypedDict) -> None:
    """Prints objects to stderr"""
    print(*objects, file=sys.stderr, **kwargs)


def _day(blob_name: str) -> int:
    """Parse day number from Blob's path

    Use the known Blob path convention to parse the day part from the path.
    The path convention is <LOG_ID>/YYYY/MM/DD/<OBJECT_NAME>
    """
    # calculated in function to allow test to set LOG_ID
    offset = len(LOG_ID) + 1 + 4 + 1 + 2 + 1
    return int(blob_name[offset : offset + 2])


def _is_valid_import_range() -> bool:
    """Validate the import date range

    Checks the import range dates to ensure that
    - start date is earlier than end date
    - no dates in the range are older than 29 days
     due to https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry#FIELDS.timestamp
    """
    if START_DATE > END_DATE:
        eprint("Start date of the import time range should be earlier than end date")
        return False
    # comment the following 3 lines if import range includes dates older than 29 days from now
    if (date.today() - START_DATE).days > 29:
        eprint("Import range includes dates older than 29 days from today.")
        return False
    return True


def calc_import_range() -> Tuple[date, date]:
    """Calculate import range for the task based on full import range and number of tasks"""
    if TASK_COUNT == 1:
        return START_DATE, END_DATE

    diff = END_DATE - START_DATE
    if diff.days > TASK_COUNT:
        shard_days = math.floor(diff.days / TASK_COUNT)
    else:
        shard_days = 1

    # start day is next day after prev. task end day
    start_date = START_DATE + timedelta((shard_days + 1) * TASK_INDEX)
    # when no more tasks required return (deterministic) negative range
    if start_date > END_DATE:
        return END_DATE, START_DATE

    if TASK_INDEX < (TASK_COUNT - 1):
        end_date = start_date + timedelta(shard_days)
    else:
        end_date = END_DATE
    return start_date, end_date


def _prefix(_date: date) -> str:
    return f"{LOG_ID}/{_date.year:04}/{_date.month:02}/"


def list_log_files(first_day: date, last_day: date, client: storage.Client) -> List:
    """Load paths to all log files stored in Cloud Storage in between first and last days.
    For log organization hierarchy see
    https://cloud.google.com/logging/docs/export/storage#gcs-organization.
    """
    paths = []

    # collect paths for special case when first and last days are in the same month
    if first_day.year == last_day.year and first_day.month == last_day.month:
        blobs = client.list_blobs(
            BUCKET_NAME, prefix=_prefix(first_day), delimiter=None
        )
        paths = [
            b.name
            for b in blobs
            if _day(b.name) >= first_day.day and _day(b.name) <= last_day.day
        ]
        return paths

    # collect all log file paths in first month and filter those for early days
    blobs = client.list_blobs(BUCKET_NAME, prefix=_prefix(first_day), delimiter=None)
    paths.extend([b.name for b in blobs if _day(b.name) >= first_day.day])
    # process all paths in last months
    blobs = client.list_blobs(BUCKET_NAME, prefix=_prefix(last_day))
    paths.extend([b.name for b in blobs if _day(b.name) <= last_day.day])
    # process all paths in between
    for year in range(first_day.year, last_day.year + 1):
        for month in range(
            first_day.month + 1 if year == first_day.year else 1,
            last_day.month if year == last_day.year else 13,
        ):
            blobs = client.list_blobs(
                BUCKET_NAME, prefix=_prefix(date(year=year, month=month, day=1))
            )
            paths.extend([b.name for b in blobs])
    return paths


def _read_logs(path: str, bucket: storage.Bucket) -> List[str]:
    blob = bucket.blob(path)
    contents = blob.download_as_string()
    return contents.splitlines()


def _write_logs(logs: List[dict], client: logging_v2.Client) -> None:
    try:
        client.logging_api.write_entries(logs)
    except exceptions.PermissionDenied as err2:
        for detail in err2.details:
            if isinstance(detail, logging_v2.types.WriteLogEntriesPartialErrors):
                # partialerrors.log_entry_errors is a dictionary
                # keyed by the logs' zero-based index in the logs.
                # consider implementing custom error handling
                eprint(f"{detail}")
        raise


def _patch_entry(log: dict, project_id: str) -> None:
    """Modify entry fields to allow importing entry to destination project.

    Save logName as a user label.
    Replace logName with the fixed value "projects/PROJECT_ID/logs/imported_logs".
    Rename the obsolete key "serviceData" with "metadata".
    """
    log_name = log.get("logName")
    labels = log.get("labels")
    log["logName"] = f"projects/{project_id}/logs/imported_logs"
    if not labels:
        labels = dict()
        log["labels"] = labels
    labels["original_logName"] = log_name
    # TODO: remove after the following issue is fixed:
    # https://github.com/googleapis/python-logging/issues/945
    if "protoPayload" in log:
        payload = log.get("protoPayload")
        if "serviceData" in payload:
            # the following line changes the place of metadata in the dictionary
            payload["metadata"] = payload.pop("serviceData")
    # uncomment the following 2 lines if import range includes dates older than 29 days from now
    # labels["original_timestamp"] = log["timestamp"]
    # log["timestamp"] = None


def import_logs(
    log_files: List, storage_client: storage.Client, logging_client: logging_v2.Client
) -> None:
    """Iterates through log files to write log entries in batched mode"""
    total_size, logs = 0, []
    bucket = storage_client.bucket(BUCKET_NAME)
    for file_path in log_files:
        data = _read_logs(file_path, bucket)
        for entry in data:
            log = json.loads(entry)
            _patch_entry(log, logging_client.project)
            size = sys.getsizeof(log)
            if total_size + size >= _LOGS_MAX_SIZE_BYTES:
                _write_logs(logs, logging_client)
                total_size, logs = 0, []
            total_size += size
            logs.append(log)
    if logs:
        _write_logs(logs, logging_client)


def main() -> None:
    """Imports logs from Cloud Storage to Cloud Logging"""
    if not START_DATE or not END_DATE or not LOG_ID or not BUCKET_NAME:
        eprint("Missing some of required parameters")
        sys.exit(1)
    if not _is_valid_import_range():
        sys.exit(1)

    start_date, end_date = calc_import_range()

    if start_date > end_date:
        print(f"Task #{(TASK_INDEX+1)} has no work to do")
        sys.exit(0)
    print(
        f"Task #{(TASK_INDEX+1)} starts importing logs from {start_date} to {end_date}"
    )

    storage_client = storage.Client()
    log_files = list_log_files(start_date, end_date, storage_client)
    logging_client = (
        logging_v2.Client(project=PROJECT_ID) if PROJECT_ID else logging_v2.Client()
    )
    import_logs(log_files, storage_client, logging_client)


# Start script
if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        eprint(f"Task #{TASK_INDEX+1}, failed: {err}")
        sys.exit(1)
