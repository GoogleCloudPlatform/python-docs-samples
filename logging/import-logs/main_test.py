# Copyright 2023 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-return-statements

from datetime import date, timedelta
import json
import os
import sys
from typing import List, Tuple, TypedDict
from unittest import mock
from unittest.mock import MagicMock

from google.cloud import logging_v2, storage
import pytest

import main

TEST_LOG_ID = "test-log"
TEST_BUCKET = "test-bucket"
TEST_BUCKET_NAME = f"gs://{TEST_BUCKET}"
TEST_PROJECT_ID = "test-project-id"


def _setup_environment(
    task_index: int = 0,
    task_count: int = 1,
    start_date: str = "01/01/0001",
    end_date: str = "01/01/0001",
    log_id: str = TEST_LOG_ID,
    storage_bucket: str = TEST_BUCKET,
    max_size: int = 0,
) -> None:
    main.LOG_ID = log_id
    main.BUCKET_NAME = storage_bucket
    main.TASK_INDEX = task_index
    main.TASK_COUNT = task_count
    main.START_DATE = start_date
    main.END_DATE = end_date
    main._LOGS_MAX_SIZE_BYTES = max_size  # pylint: disable=protected-access


@pytest.mark.parametrize(
    "start_date, end_date, expected_validity",
    [
        (date.today() - timedelta(days=29), date.today() - timedelta(days=10), True),
        (date.today() - timedelta(days=10), date.today() - timedelta(days=29), False),
        (date.today() - timedelta(days=30), date.today(), False),
        ("07/01/2023", "06/01/2023", False),
    ],
    ids=[
        "valid range",
        "invalid range: start later than end",
        "invalid range: start older than 29 days",
        "invalid range: end older than 29 days",
    ],
)
def test_import_range_validation(
    start_date: str, end_date: str, expected_validity: bool
) -> None:
    _setup_environment(
        start_date=start_date,
        end_date=end_date,
    )
    isvalid = main._is_valid_import_range()  # pylint: disable=protected-access
    assert (
        isvalid == expected_validity
    ), f"import range ({start_date} -> {end_date}) validation failed: expected {expected_validity} and got {isvalid}"


@pytest.mark.parametrize(
    "start_date, end_date, task_index, task_count, expected_first_day, expected_last_day",
    [
        (
            date(2001, 1, 1),
            date(2001, 1, 31),
            0,
            1,
            date(2001, 1, 1),
            date(2001, 1, 31),
        ),
        (
            date(2001, 1, 1),
            date(2001, 1, 10),
            0,
            20,
            date(2001, 1, 1),
            date(2001, 1, 2),
        ),
        (
            date(2001, 1, 1),
            date(2001, 1, 10),
            12,
            20,
            date(2001, 1, 10),
            date(2001, 1, 1),
        ),
        (
            date(2001, 1, 10),
            date(2001, 2, 1),
            0,
            2,
            date(2001, 1, 10),
            date(2001, 1, 21),
        ),
        (
            date(2001, 1, 10),
            date(2001, 2, 1),
            1,
            2,
            date(2001, 1, 22),
            date(2001, 2, 1),
        ),
        (date(2001, 5, 5), date(2002, 2, 2), 1, 2, date(2001, 9, 19), date(2002, 2, 2)),
    ],
    ids=[
        "simple single range",
        "more tasks than days",
        "extra task when more tasks then days",
        "two month range task 1",
        "two month range task 2",
        "multi year range",
    ],
)
def test_calc_import_range(
    start_date: str,
    end_date: str,
    task_index: int,
    task_count: int,
    expected_first_day: date,
    expected_last_day: date,
) -> None:
    _setup_environment(
        task_index=task_index,
        task_count=task_count,
        start_date=start_date,
        end_date=end_date,
    )

    first_day, last_day = main.calc_import_range()

    assert (
        first_day == expected_first_day
    ), f"first day is wrong: expected {expected_first_day} and got {first_day}"
    assert (
        last_day == expected_last_day
    ), f"last day is wrong: expected {expected_last_day} and got {last_day}"


TEST_FILES_JUN_2001 = [
    storage.Blob(name=f"{TEST_LOG_ID}/2001/06/01/file1.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2001/06/01/file2.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2001/06/02/file1.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2001/06/02/file2.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2001/06/03/file1.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2001/06/03/file2.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2001/06/04/file2.json", bucket=TEST_BUCKET),
]
TEST_FILES_JUL_2001 = [
    storage.Blob(name=f"{TEST_LOG_ID}/2001/07/01/file1.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2001/07/01/file2.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2001/07/02/file1.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2001/07/02/file2.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2001/07/03/file1.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2001/07/03/file2.json", bucket=TEST_BUCKET),
]
TEST_FILES_AUG_2001 = [
    storage.Blob(name=f"{TEST_LOG_ID}/2001/08/01/file1.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2001/08/01/file2.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2001/08/02/file1.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2001/08/02/file2.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2001/08/03/file1.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2001/08/03/file2.json", bucket=TEST_BUCKET),
]
TEST_FILES_MAY_2002 = [
    storage.Blob(name=f"{TEST_LOG_ID}/2002/05/01/file1.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2002/05/01/file2.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2002/05/02/file1.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2002/05/02/file2.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2002/05/03/file1.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2002/05/03/file2.json", bucket=TEST_BUCKET),
]
TEST_FILES_JAN_2003 = [
    storage.Blob(name=f"{TEST_LOG_ID}/2003/01/01/file1.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2003/01/01/file2.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2003/01/02/file1.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2003/01/02/file2.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2003/01/03/file1.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2003/01/03/file2.json", bucket=TEST_BUCKET),
]
TEST_FILES_FEB_2003 = [
    storage.Blob(name=f"{TEST_LOG_ID}/2003/02/01/file1.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2003/02/01/file2.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2003/02/02/file1.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2003/02/02/file2.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2003/02/03/file1.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2003/02/03/file2.json", bucket=TEST_BUCKET),
]
TEST_FILES_MAR_2003 = [
    storage.Blob(name=f"{TEST_LOG_ID}/2003/03/01/file1.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2003/03/01/file2.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2003/03/02/file1.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2003/03/02/file2.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2003/03/03/file1.json", bucket=TEST_BUCKET),
    storage.Blob(name=f"{TEST_LOG_ID}/2003/03/03/file2.json", bucket=TEST_BUCKET),
]


def _args_based_list_blobs_return(*_args: str, **kwargs: TypedDict) -> List[str]:
    if kwargs["prefix"] == f"{TEST_LOG_ID}/2001/06/":
        print("TEST_FILES_JUN_2001")
        return TEST_FILES_JUN_2001
    elif kwargs["prefix"] == f"{TEST_LOG_ID}/2001/07/":
        print("TEST_FILES_JUL_2001")
        return TEST_FILES_JUL_2001
    elif kwargs["prefix"] == f"{TEST_LOG_ID}/2001/08/":
        print("TEST_FILES_AUG_2001")
        return TEST_FILES_AUG_2001
    elif kwargs["prefix"] == f"{TEST_LOG_ID}/2002/05/":
        print("TEST_FILES_MAY_2002")
        return TEST_FILES_MAY_2002
    elif kwargs["prefix"] == f"{TEST_LOG_ID}/2003/01/":
        print("TEST_FILES_JAN_2003")
        return TEST_FILES_JAN_2003
    elif kwargs["prefix"] == f"{TEST_LOG_ID}/2003/02/":
        print("TEST_FILES_FEB_2003")
        return TEST_FILES_FEB_2003
    elif kwargs["prefix"] == f"{TEST_LOG_ID}/2003/03/":
        print("TEST_FILES_MAR_2003")
        return TEST_FILES_MAR_2003
    else:
        return []


@pytest.mark.parametrize(
    "first_day, last_day, expected_paths",
    [
        (date(2001, 6, 1), date(2001, 6, 30), [f.name for f in TEST_FILES_JUN_2001]),
        (
            date(2001, 6, 2),
            date(2001, 6, 3),
            [f.name for f in TEST_FILES_JUN_2001[2:-1]],
        ),
        (
            date(2001, 7, 3),
            date(2003, 2, 2),
            [
                f.name
                for f in [
                    *TEST_FILES_JUL_2001[-2:],
                    *TEST_FILES_AUG_2001,
                    *TEST_FILES_MAY_2002,
                    *TEST_FILES_JAN_2003,
                    *TEST_FILES_FEB_2003[:-2],
                ]
            ],
        ),
    ],
    ids=["simple one month range", "subrange of one month", "cross year range"],
)
def test_list_log_files(first_day: str, last_day: str, expected_paths: List) -> None:
    _setup_environment()

    mocked_client = MagicMock(spec=storage.Client)
    mocked_client.list_blobs = MagicMock(side_effect=_args_based_list_blobs_return)

    paths = main.list_log_files(first_day, last_day, mocked_client)

    assert set(paths) == set(expected_paths)


TEST_LOG_FILES = ["file1.json", "file2.json", "file3.json", "file4.json"]
TEST_CONTENT = {
    "file1.json": '{"file": "1", "line": "1"}\n{"file": "1", "line": "2"}\n{"file": "1", "line": "3"}',
    "file2.json": '{"file": "2", "line": "1"}\n{"file": "2", "line": "2"}',
    "file3.json": '{"file": "3", "line": "1"}\n{"file": "3", "line": "2"}\n\
         {"file": "3", "line": "3"}\n{"file": "3", "line": "4"}',
    "file4.json": '{"file": "4", "line": "1"}',
}
# note that all log entries are of same size (expected 184 bytes)
TEST_LOG_SIZE = sys.getsizeof(json.loads(TEST_CONTENT["file4.json"]))


def _args_based_blob_return(*args: Tuple, **_kwargs: TypedDict) -> str:
    mocked_blob = MagicMock(spec=storage.Blob)
    mocked_blob.download_as_string = MagicMock(return_value=TEST_CONTENT.get(args[0]))
    return mocked_blob


def _calc_args_size(*args: Tuple) -> int:
    size = 0
    if args and args[0] and isinstance(args[0][0], list):
        for arg in args[0][0]:
            size += sys.getsizeof(arg)
    return size


@pytest.mark.parametrize(
    "log_files, max_size, expected_writes",
    [
        (TEST_LOG_FILES, 1 * 1024 * 1024, [(10 * TEST_LOG_SIZE)]),
        (
            TEST_LOG_FILES[:2],
            (TEST_LOG_SIZE + 10),
            [TEST_LOG_SIZE, TEST_LOG_SIZE, TEST_LOG_SIZE, TEST_LOG_SIZE, TEST_LOG_SIZE],
        ),
        (
            TEST_LOG_FILES[:3],
            (4 * TEST_LOG_SIZE + 10),
            [4 * TEST_LOG_SIZE, 4 * TEST_LOG_SIZE, TEST_LOG_SIZE],
        ),
    ],
    ids=[
        "read all, write once",
        "read few files, write many times",
        "read many files, write fewer times",
    ],
)
def test_import_logs(
    log_files: List[str], max_size: int, expected_writes: List[int]
) -> None:
    _setup_environment(max_size=max_size)
    mocked_storage_client = MagicMock(spec=storage.Client)
    mocked_bucket = MagicMock(spec=storage.Bucket)
    mocked_storage_client.bucket = MagicMock(return_value=mocked_bucket)
    mocked_bucket.blob = MagicMock(side_effect=_args_based_blob_return)
    mocked_logging_client = MagicMock(spec=logging_v2.Client)
    mocked_logging_client.logging_api = MagicMock()
    mocked_logging_client.project = TEST_PROJECT_ID
    mocked_write_entries = mocked_logging_client.logging_api.write_entries = MagicMock()

    main.import_logs(log_files, mocked_storage_client, mocked_logging_client)

    assert mocked_bucket.blob.call_count == len(
        log_files
    ), f"expected {len(log_files)} reads, got {mocked_bucket.blob.call_count}"
    assert len(mocked_write_entries.call_args_list) == len(
        expected_writes
    ), f"expected {len(expected_writes)} writes, got {len(mocked_write_entries.call_args_list)}"
    for write_call, expected_size in zip(
        mocked_write_entries.call_args_list, expected_writes
    ):
        assert (
            _calc_args_size(write_call.args) == expected_size
        ), f"expected write size {expected_size}, got {_calc_args_size(write_call.args)}"


TEST_DATE_STR = "08/12/2023"


@mock.patch.dict(os.environ, {"TEST_DATE": TEST_DATE_STR}, clear=True)
def test_parse_date() -> None:
    test_date = main.getenv_date("TEST_DATE")
    test_date_str = test_date.strftime("%m/%d/%Y")
    assert (
        test_date_str == TEST_DATE_STR
    ), f"expected {TEST_DATE_STR}, got {test_date_str}"


TEST_LOG_WITH_SERVICEDATA = {
    "logName": "projects/someproject/logs/somelog",
    "protoPayload": {
        "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
        "authenticationInfo": {
            "principalEmail": "service@gcp-sa-scc-notification.iam.gserviceaccount.com"
        },
        "authorizationInfo": [
            {
                "granted": True,
                "permission": "bigquery.tables.update",
                "resource": "projects/someproject/datasets/someds/tables/sometbl",
                "resourceAttributes": {}
            }
        ],
        "serviceData": {
            '@type': 'type.googleapis.com/google.cloud.bigquery.logging.v1.AuditData',
            'tableUpdateRequest': {
                'resource': {
                    'info': {},
                    'schemaJson': '{}',
                    'updateTime': '2024-08-20T15:01:48.399Z',
                    'view': {}
                }
            }
        },
        "methodName": "google.cloud.bigquery.v2.TableService.PatchTable",
        "requestMetadata": {
            "callerIp": "private",
            "destinationAttributes": {},
            "requestAttributes": {}
        },
        "resourceName": "projects/someproject/datasets/someds/tables/sometbl",
        "serviceName": "bigquery.googleapis.com",
        "status": {}
    },
    "resource": {
        "labels": {
            "dataset_id": "someds",
            "project_id": "someproject"
        },
        "type": "bigquery_dataset"
    },
    "severity": "NOTICE",
}
TEST_LOG_WITH_PATCHED_SERVICEDATA = {
    "logName": f"projects/{TEST_PROJECT_ID}/logs/imported_logs",
    "protoPayload": {
        "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
        "authenticationInfo": {
            "principalEmail": "service@gcp-sa-scc-notification.iam.gserviceaccount.com"
        },
        "authorizationInfo": [
            {
                "granted": True,
                "permission": "bigquery.tables.update",
                "resource": "projects/someproject/datasets/someds/tables/sometbl",
                "resourceAttributes": {}
            }
        ],
        # this field is renamed from 'serviceData'
        "metadata": {
            '@type': 'type.googleapis.com/google.cloud.bigquery.logging.v1.AuditData',
            'tableUpdateRequest': {
                'resource': {
                    'info': {},
                    'schemaJson': '{}',
                    'updateTime': '2024-08-20T15:01:48.399Z',
                    'view': {}
                }
            }
        },
        "methodName": "google.cloud.bigquery.v2.TableService.PatchTable",
        "requestMetadata": {
            "callerIp": "private",
            "destinationAttributes": {},
            "requestAttributes": {}
        },
        "resourceName": "projects/someproject/datasets/someds/tables/sometbl",
        "serviceName": "bigquery.googleapis.com",
        "status": {}
    },
    "resource": {
        "labels": {
            "dataset_id": "someds",
            "project_id": "someproject"
        },
        "type": "bigquery_dataset"
    },
    "labels": {
        "original_logName": "projects/someproject/logs/somelog",
    },
    "severity": "NOTICE",
}


def test_patch_serviceData_field() -> None:
    log = dict(TEST_LOG_WITH_SERVICEDATA)
    main._patch_entry(log, TEST_PROJECT_ID)

    assert (log == TEST_LOG_WITH_PATCHED_SERVICEDATA)
