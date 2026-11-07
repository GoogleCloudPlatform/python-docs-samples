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

# [START cloudscheduler_pause_job]
import sys

from google.api_core import exceptions
from google.cloud import scheduler_v1


def pause_job(project_id: str, location_id: str, job_id: str) -> None:
    """Pauses a job so that it stops running on its schedule.

    A paused job keeps its configuration and doesn't run until you resume it.

    Args:
        project_id: The Google Cloud project ID (for example, 'example-project-id').
        location_id: The region of the job (for example, 'us-central1').
        job_id: The ID of the job (for example, 'example-job-id').
    """
    client = scheduler_v1.CloudSchedulerClient()
    name = f"projects/{project_id}/locations/{location_id}/jobs/{job_id}"
    request = scheduler_v1.PauseJobRequest(name=name)

    # Cloud Scheduler applies one change to a job at a time. If another change
    # is still in progress, this call fails with ABORTED; retry after a few
    # seconds.
    try:
        response = client.pause_job(request=request)
    except exceptions.NotFound as err:
        print(
            f"error: job '{job_id}' not found in location '{location_id}' "
            f"for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to pause job '{job_id}' in location '{location_id}' "
            f"for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {response.name}")
        print(f"Schedule: {response.schedule}")
        print(f"State: {response.state.name}")


# [END cloudscheduler_pause_job]


if __name__ == "__main__":
    import argparse
    import os

    # Each flag defaults to its environment variable, then to an example value.
    parser = argparse.ArgumentParser(description=pause_job.__doc__.splitlines()[0])
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

    pause_job(
        project_id=args.project_id,
        location_id=args.location_id,
        job_id=args.job_id,
    )
