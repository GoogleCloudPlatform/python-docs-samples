# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START cloudscheduler_delete_job]

from google.cloud import scheduler_v1


def delete_scheduler_job(project_id: str, location_id: str, job_id: str) -> None:
    """Delete a job via the Cloud Scheduler API.

    Args:
        project_id: The Google Cloud project id.
        location_id: The location for the job to delete.
        job_id: The id of the job to delete.
    """

    # Create a client.
    client = scheduler_v1.CloudSchedulerClient()

    # Use the client to send the job deletion request.
    client.delete_job(
        scheduler_v1.DeleteJobRequest(
            name=client.job_path(project_id, location_id, job_id)
        )
    )


# [END cloudscheduler_delete_job]
