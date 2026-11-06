# Copyright 2019 Google LLC
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

# [START cloudscheduler_create_appengine_job]
import datetime
import sys

from google.api_core import exceptions
from google.cloud import scheduler_v1


def create_appengine_job(project_id: str, location_id: str, job_id: str) -> None:
    """Creates a job that sends requests to an App Engine service on a schedule.

    Args:
        project_id: The Google Cloud project ID (for example, 'example-project-id').
        location_id: The region of the project's App Engine app (for example,
            'us-central1').
        job_id: The ID for the new job (for example, 'example-job-id').
    """
    client = scheduler_v1.CloudSchedulerClient()
    # App Engine targets must be in the same project and region as the
    # App Engine app.
    parent = f"projects/{project_id}/locations/{location_id}"

    app_engine_routing = scheduler_v1.AppEngineRouting(service="default")
    app_engine_target = scheduler_v1.AppEngineHttpTarget(
        app_engine_routing=app_engine_routing,
        relative_uri="/example-handler",
        http_method=scheduler_v1.HttpMethod.POST,
        body=b"example-payload",
    )
    job = scheduler_v1.Job(
        name=f"{parent}/jobs/{job_id}",
        app_engine_http_target=app_engine_target,
        # Runs every Monday at 09:00. UTC avoids skipped or repeated runs when
        # daylight saving time starts or ends.
        schedule="0 9 * * 1",
        time_zone="UTC",
        # Cloud Scheduler reports a failure if the handler doesn't respond
        # within this deadline.
        attempt_deadline=datetime.timedelta(minutes=5),
    )
    request = scheduler_v1.CreateJobRequest(parent=parent, job=job)

    try:
        response = client.create_job(request=request)
    except exceptions.AlreadyExists as err:
        print(
            f"error: job '{job_id}' already exists in location '{location_id}' "
            f"for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to create job '{job_id}' in location '{location_id}' "
            f"for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {response.name}")
        print(f"Schedule: {response.schedule}")
        print(f"State: {response.state.name}")
        print(f"Time Zone: {response.time_zone}")


# [END cloudscheduler_create_appengine_job]


if __name__ == "__main__":
    import os

    def arg(index: int, env_var: str, default: str) -> str:
        """Reads an environment variable, then a CLI argument, then a default."""
        cli_value = sys.argv[index] if len(sys.argv) > index else None
        return os.environ.get(env_var) or cli_value or default

    create_appengine_job(
        project_id=arg(1, "GOOGLE_CLOUD_PROJECT", "example-project-id"),
        location_id=arg(2, "GOOGLE_CLOUD_LOCATION", "us-central1"),
        job_id=arg(3, "SCHEDULER_JOB_ID", "example-job-id"),
    )
