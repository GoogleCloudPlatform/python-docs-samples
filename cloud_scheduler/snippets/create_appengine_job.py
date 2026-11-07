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
    # Must be the App Engine app's project and region.
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
        # Every Monday at 09:00 UTC, which has no daylight saving shifts.
        schedule="0 9 * * 1",
        time_zone="UTC",
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
    import argparse
    import os

    # Each flag defaults to its environment variable, then to an example value.
    parser = argparse.ArgumentParser(
        description=create_appengine_job.__doc__.splitlines()[0]
    )
    parser.add_argument(
        "--project-id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
        help="Google Cloud project ID (default: $GOOGLE_CLOUD_PROJECT)",
    )
    parser.add_argument(
        "--location-id",
        default=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
        help="Region of the job (default: $GOOGLE_CLOUD_LOCATION)",
    )
    parser.add_argument(
        "--job-id",
        default=os.environ.get("SCHEDULER_JOB_ID", "example-job-id"),
        help="ID of the job (default: $SCHEDULER_JOB_ID)",
    )
    args = parser.parse_args()

    create_appengine_job(
        project_id=args.project_id,
        location_id=args.location_id,
        job_id=args.job_id,
    )
