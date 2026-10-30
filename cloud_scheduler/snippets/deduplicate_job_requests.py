# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Demonstrates how to deduplicate retried Cloud Scheduler HTTP requests.
See https://docs.cloud.google.com/scheduler/docs/configuring/deduplicate-job-requests
"""

# [START cloudscheduler_deduplicate_job_requests]
import datetime
import re

import flask
from google.api_core.exceptions import AlreadyExists
from google.cloud import firestore

db = firestore.Client()
JOB_ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,500}$")
# Set LOCK_TTL to at least your job's retry window (maxRetryDuration) so a
# Firestore TTL policy can asynchronously clean up old records. Because
# Firestore TTL deletion isn't instantaneous, if an instance terminates
# unexpectedly (for example, due to an out-of-memory error or SIGKILL) before
# doc_ref.delete() runs, the record remains IN_PROGRESS until cleaned up (unless
# you also check a lease expiration timestamp in a transaction).
LOCK_TTL = datetime.timedelta(hours=24)


def run_job_logic() -> None:
    """Replace with your job processing logic."""
    pass


def handle_scheduled_job(request: flask.Request) -> tuple[str, int]:
    """Deduplicates retried Cloud Scheduler requests using Firestore.

    Args:
        request: The incoming Flask HTTP request object.

    Returns:
        A tuple containing the response body and HTTP status code.
    """
    # Assumes the endpoint requires authentication (such as OIDC); these headers
    # aren't authenticated.
    # request.headers in Flask and Functions Framework performs case-insensitive
    # lookups automatically.
    job_name = request.headers.get("X-CloudScheduler-JobName")
    schedule_time = request.headers.get("X-CloudScheduler-ScheduleTime")

    # X-CloudScheduler-ScheduleTime is only sent for scheduled runs in
    # unix-cron format. Jobs using groc schedules omit this header, and manual
    # triggers (gcloud scheduler jobs run or "Force a job run") might omit it
    # or reuse a scheduled timestamp. To allow manual runs when schedule_time
    # is omitted, run run_job_logic() directly when job_name is valid and
    # schedule_time is None.
    if not job_name or not schedule_time:
        return ("Missing Cloud Scheduler headers", 400)

    # Validate the job ID (prevent "/" path traversal) and normalize the
    # RFC 3339 timestamp to UTC so equivalent offsets map to the same key.
    if not JOB_ID_RE.fullmatch(job_name):
        return ("Invalid X-CloudScheduler-JobName header", 400)
    try:
        parsed_time = datetime.datetime.fromisoformat(
            schedule_time.replace("Z", "+00:00")
        )
        if parsed_time.tzinfo is None:
            return (
                "X-CloudScheduler-ScheduleTime must include a timezone",
                400,
            )
        normalized_time = parsed_time.astimezone(
            datetime.timezone.utc
        ).strftime("%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return ("Invalid X-CloudScheduler-ScheduleTime header", 400)

    # If this endpoint receives jobs from multiple projects or regions, also
    # validate and include the project ID or region in dedup_key.
    dedup_key = f"{job_name}:{normalized_time}"
    doc_ref = db.collection("scheduler_dedup").document(dedup_key)
    now = datetime.datetime.now(datetime.timezone.utc)

    try:
        # create() is atomic and raises AlreadyExists if the document exists.
        doc_ref.create(
            {
                "job_name": job_name,
                "schedule_time": normalized_time,
                "status": "IN_PROGRESS",
                "created_at": now,
                "expires_at": now + LOCK_TTL,
            }
        )
    except AlreadyExists:
        # Firestore returns ALREADY_EXISTS (HTTP 409 Conflict) if the document
        # already exists.
        doc = doc_ref.get()
        if doc.exists and doc.to_dict().get("status") == "COMPLETED":
            # A previous attempt already succeeded. Return 200 OK so Cloud
            # Scheduler stops retrying.
            return ("Duplicate job request ignored", 200)
        # Another attempt is still running. Return 409 Conflict so Cloud
        # Scheduler keeps its retry policy active if that attempt fails.
        return ("Job execution already in progress", 409)

    try:
        run_job_logic()
    except BaseException:
        # If the job logic fails or is terminated (such as by SystemExit),
        # delete the lock document and re-raise so a subsequent retry can run.
        doc_ref.delete()
        raise

    doc_ref.update({"status": "COMPLETED"})
    return ("Job completed", 200)
# [END cloudscheduler_deduplicate_job_requests]
