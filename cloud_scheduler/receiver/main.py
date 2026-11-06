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
import json
import threading

import flask
import functions_framework

# Cloud Scheduler can deliver the same scheduled run more than once, sometimes
# at nearly the same time, so the function claims each run before doing its
# work. These in-memory claims last only for the life of one instance. In
# production, claim each run with a single atomic write, such as creating a
# Firestore document that fails if the document already exists.
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
    """Handles a request that a Cloud Scheduler job sends to this function.

    Deploy the function to require authentication. Cloud Run functions then
    verifies the job's OIDC token before the request reaches this
    function, and only service accounts with the Cloud Run Invoker role can
    call it.
    """
    job_name = request.headers.get("X-CloudScheduler-JobName")
    schedule_time = request.headers.get("X-CloudScheduler-ScheduleTime")
    if not job_name or not schedule_time:
        return "error: missing Cloud Scheduler headers", 400

    # The schedule time stays the same when Cloud Scheduler retries a run,
    # so the job name and schedule time identify a single scheduled run.
    run_key = f"{job_name}/{schedule_time}"

    # Check and claim the run in one step, so that two deliveries of the same
    # run that arrive together can't both do the work.
    with claimed_runs_lock:
        if run_key in claimed_runs:
            log("Skipped duplicate run", jobName=job_name, scheduleTime=schedule_time)
            return "Duplicate run skipped", 200
        claimed_runs.add(run_key)

    # Finish the work within the job's attempt deadline. Cloud Scheduler
    # treats a slow response as a failure even if the work later succeeds.
    try:
        process_run(job_name, schedule_time, request.get_data(as_text=True))
    except Exception:
        # Release the claim so that a retry can process the run. Re-raising
        # returns HTTP 500, which tells Cloud Scheduler to retry the run
        # according to the job's retry settings.
        with claimed_runs_lock:
            claimed_runs.discard(run_key)
        raise
    return "Run processed", 200


# [END cloudscheduler_receiver]
