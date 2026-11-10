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

# [START cloudscheduler_receiver]
import datetime
import json
import threading

import flask
import functions_framework

# Duplicate deliveries of a run are skipped. Use a durable store, such as
# Firestore, across instances.
claimed_runs: set[str] = set()
claimed_runs_lock = threading.Lock()


def log(message: str, **fields: str) -> None:
    """Writes a structured log entry that Cloud Logging parses from stdout."""
    print(json.dumps({"severity": "INFO", "message": message, **fields}))


def process_run(job_name: str, schedule_time: str, payload: str) -> None:
    """Does the scheduled work. Replace the body with your own task."""
    log(
        "Processed scheduled run",
        jobName=job_name,
        scheduleTime=schedule_time,
        payload=payload,
    )


@functions_framework.http
def handle_scheduled_run(request: flask.Request) -> tuple[str, int]:
    """Handles a Cloud Scheduler request.

    Cloud Run functions verifies the job's OIDC token.
    """
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
    run_key = f"{job_name}/{minute}"

    # Check and claim in one step so concurrent duplicates can't both run.
    with claimed_runs_lock:
        if run_key in claimed_runs:
            log("Skipped duplicate run", jobName=job_name, scheduleTime=schedule_time)
            return "Duplicate run skipped", 200
        claimed_runs.add(run_key)

    # Finish within the job's attempt deadline.
    try:
        process_run(job_name, schedule_time, request.get_data(as_text=True))
    except Exception:
        # Release the claim; the 500 response makes Cloud Scheduler retry.
        with claimed_runs_lock:
            claimed_runs.discard(run_key)
        raise
    return "Run processed", 200


# [END cloudscheduler_receiver]
