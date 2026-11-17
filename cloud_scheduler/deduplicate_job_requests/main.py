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

# [START cloudscheduler_deduplicate_job_requests]
import datetime
import hashlib
import uuid

import flask
import functions_framework
from google.cloud import firestore

# Longer than the work takes, and at least the job's attempt deadline.
LEASE = datetime.timedelta(minutes=5)
# Keep records past the job's retry window. A TTL policy on expire_at deletes them.
RETENTION = datetime.timedelta(days=1)

db = firestore.Client()


def run_job_logic() -> None:
    """Does the scheduled work. Replace the body with your own task."""


@firestore.transactional
def claim_run(
    transaction: firestore.Transaction,
    run_ref: firestore.DocumentReference,
    attempt_id: str,
    now: datetime.datetime,
) -> str:
    """Claims the run unless it's done or another attempt holds the lease."""
    snapshot = run_ref.get(transaction=transaction)
    if snapshot.exists:
        run = snapshot.to_dict()
        if run["status"] == "completed":
            return "completed"
        if run["lease_expires"] > now:
            return "in_progress"
    transaction.set(
        run_ref,
        {
            "status": "in_progress",
            "attempt_id": attempt_id,
            "lease_expires": now + LEASE,
            "expire_at": now + RETENTION,
        },
    )
    return "claimed"


@firestore.transactional
def finish_run(
    transaction: firestore.Transaction,
    run_ref: firestore.DocumentReference,
    attempt_id: str,
    succeeded: bool,
) -> None:
    """Completes or releases the run, if this attempt still holds the claim."""
    snapshot = run_ref.get(transaction=transaction)
    if not snapshot.exists or snapshot.to_dict().get("attempt_id") != attempt_id:
        return  # A retry claimed the run after this attempt's lease expired.
    if succeeded:
        transaction.update(run_ref, {"status": "completed"})
    else:
        transaction.delete(run_ref)


@functions_framework.http
def handle_scheduled_job(request: flask.Request) -> tuple[str, int]:
    """Runs a job's work once per scheduled run, even if the run is delivered twice."""
    job_name = request.headers.get("X-CloudScheduler-JobName")
    schedule_time = request.headers.get("X-CloudScheduler-ScheduleTime")
    if not job_name or not schedule_time:
        return "error: missing Cloud Scheduler headers", 400

    # Key on the minute; some deliveries omit the few-second offset.
    try:
        scheduled = datetime.datetime.fromisoformat(schedule_time)
    except ValueError:
        return "error: invalid X-CloudScheduler-ScheduleTime header", 400
    minute = scheduled.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    run_id = hashlib.sha256(f"{job_name}/{minute}".encode()).hexdigest()
    run_ref = db.collection("scheduler_runs").document(run_id)
    now = datetime.datetime.now(datetime.timezone.utc)
    attempt_id = uuid.uuid4().hex

    status = claim_run(db.transaction(), run_ref, attempt_id, now)
    if status == "completed":
        return "Duplicate run skipped", 200
    if status == "in_progress":
        # A non-2xx response keeps retries going in case that attempt fails.
        return "Run in progress", 409

    try:
        run_job_logic()
    except Exception:
        # Releases the claim so that a retry can process the run.
        finish_run(db.transaction(), run_ref, attempt_id, succeeded=False)
        raise
    finish_run(db.transaction(), run_ref, attempt_id, succeeded=True)
    return "Run processed", 200


# [END cloudscheduler_deduplicate_job_requests]
