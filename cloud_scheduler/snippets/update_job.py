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

# [START cloudscheduler_update_job]
import sys

from google.api_core import exceptions
from google.cloud import scheduler_v1
from google.protobuf import field_mask_pb2


def update_job(project_id: str, location_id: str, job_id: str) -> None:
    """Changes the schedule of an existing job.

    Args:
        project_id: The Google Cloud project ID (for example, 'example-project-id').
        location_id: The region of the job (for example, 'us-central1').
        job_id: The ID of the job to update (for example, 'example-job-id').
    """
    client = scheduler_v1.CloudSchedulerClient()
    name = f"projects/{project_id}/locations/{location_id}/jobs/{job_id}"

    # Runs every weekday at 10:00 UTC.
    job = scheduler_v1.Job(name=name, schedule="0 10 * * 1-5", time_zone="UTC")
    # Only the fields in the update mask change; the job keeps its other
    # settings, such as its target.
    update_mask = field_mask_pb2.FieldMask(paths=["schedule", "time_zone"])
    request = scheduler_v1.UpdateJobRequest(job=job, update_mask=update_mask)

    # Cloud Scheduler applies one change to a job at a time. If another change
    # is still in progress, this call fails with ABORTED; retry after a few
    # seconds.
    try:
        response = client.update_job(request=request)
    except exceptions.NotFound as err:
        print(
            f"error: job '{job_id}' not found in location '{location_id}' "
            f"for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to update job '{job_id}' in location '{location_id}' "
            f"for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {response.name}")
        print(f"Schedule: {response.schedule}")
        print(f"State: {response.state.name}")
        print(f"Time Zone: {response.time_zone}")


# [END cloudscheduler_update_job]


if __name__ == "__main__":
    import os

    def arg(index: int, env_var: str, default: str) -> str:
        """Reads an environment variable, then a CLI argument, then a default."""
        cli_value = sys.argv[index] if len(sys.argv) > index else None
        return os.environ.get(env_var) or cli_value or default

    update_job(
        project_id=arg(1, "GOOGLE_CLOUD_PROJECT", "example-project-id"),
        location_id=arg(2, "GOOGLE_CLOUD_LOCATION", "us-central1"),
        job_id=arg(3, "SCHEDULER_JOB_ID", "example-job-id"),
    )
