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

import flask
import functions_framework

# Cloud Scheduler can deliver the same scheduled run more than once, so the
# function records which runs it has finished. This in-memory set only lasts
# for the life of one instance; store run keys in a durable database such as
# Firestore so that every instance sees them.
processed_runs: set[str] = set()


def log(message: str, **fields: str) -> None:
    """Writes a structured log entry that Cloud Logging parses from stdout."""
    print(json.dumps({"severity": "INFO", "message": message, **fields}))


@functions_framework.http
def handle_scheduled_run(request: flask.Request) -> tuple[str, int]:
    """Handles a request that a Cloud Scheduler job sends to this function.

    Deploy the function without unauthenticated access. Cloud Run functions
    then verifies the job's OIDC token before the request reaches this
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
    if run_key in processed_runs:
        log("Skipped duplicate run", jobName=job_name, scheduleTime=schedule_time)
        return "Run already processed", 200

    # Finish the work within the job's attempt deadline. Cloud Scheduler
    # treats a slow response as a failure even if the work later succeeds.
    # If the work raises an exception, the function returns HTTP 500, which
    # tells Cloud Scheduler to retry the run according to the job's retry
    # settings.
    payload = request.get_data(as_text=True)
    log(
        "Processed scheduled run",
        jobName=job_name,
        scheduleTime=schedule_time,
        payload=payload,
    )
    processed_runs.add(run_key)
    return "Run processed", 200


# [END cloudscheduler_receiver]
