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

# [START cloudscheduler_list_jobs]
import sys

from google.api_core import exceptions
from google.cloud import scheduler_v1


def list_jobs(project_id: str, location_id: str) -> None:
    """Lists the jobs in a location, with each job's schedule and state.

    Args:
        project_id: The Google Cloud project ID (for example, 'example-project-id').
        location_id: The region to list jobs in (for example, 'us-central1').
    """
    client = scheduler_v1.CloudSchedulerClient()
    parent = f"projects/{project_id}/locations/{location_id}"
    request = scheduler_v1.ListJobsRequest(parent=parent)

    try:
        # The client fetches more pages as the loop needs them.
        for job in client.list_jobs(request=request):
            print(f"Resource ID: {job.name}")
            print(f"Schedule: {job.schedule}")
            print(f"State: {job.state.name}")
    except exceptions.InvalidArgument as err:
        print(
            f"error: invalid location '{location_id}' for project "
            f"'{project_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to list jobs in location '{location_id}' for project "
            f"'{project_id}': {err.message}",
            file=sys.stderr,
        )


# [END cloudscheduler_list_jobs]


if __name__ == "__main__":
    import os

    def arg(index: int, env_var: str, default: str) -> str:
        """Reads an environment variable, then a CLI argument, then a default."""
        cli_value = sys.argv[index] if len(sys.argv) > index else None
        return os.environ.get(env_var) or cli_value or default

    list_jobs(
        project_id=arg(1, "GOOGLE_CLOUD_PROJECT", "example-project-id"),
        location_id=arg(2, "GOOGLE_CLOUD_LOCATION", "us-central1"),
    )
