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

# [START cloudscheduler_run_job]
import sys

from google.api_core import exceptions
from google.cloud import scheduler_v1


def run_job(project_id: str, location_id: str, job_id: str) -> None:
    """Runs a job immediately, outside its schedule.

    Running a job doesn't change its schedule. Use it to test a job's
    target and authentication without waiting for the next scheduled run.

    Args:
        project_id: The Google Cloud project ID (for example, 'example-project-id').
        location_id: The region of the job (for example, 'us-central1').
        job_id: The ID of the job (for example, 'example-job-id').
    """
    client = scheduler_v1.CloudSchedulerClient()
    name = f"projects/{project_id}/locations/{location_id}/jobs/{job_id}"
    request = scheduler_v1.RunJobRequest(name=name)

    try:
        response = client.run_job(request=request)
    except exceptions.NotFound as err:
        print(
            f"error: job '{job_id}' not found in location '{location_id}' "
            f"for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to run job '{job_id}' in location '{location_id}' "
            f"for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {response.name}")
        print(f"Schedule: {response.schedule}")
        print(f"State: {response.state.name}")


# [END cloudscheduler_run_job]


if __name__ == "__main__":
    import argparse
    import os

    # Each flag defaults to its environment variable, then to an example value.
    parser = argparse.ArgumentParser(description=run_job.__doc__.splitlines()[0])
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

    run_job(
        project_id=args.project_id,
        location_id=args.location_id,
        job_id=args.job_id,
    )
