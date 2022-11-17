#  Copyright 2022 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# [START batch_delete_job]
from google.api_core.operation import Operation

from google.cloud import batch_v1


def delete_job(project_id: str, region: str, job_name: str) -> Operation:
    """
    Triggers the deletion of a Job.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        region: name of the region hosts the job.
        job_name: the name of the job that you want to delete.

    Returns:
        An operation object related to the deletion. You can call `.result()`
        on it to wait for its completion.
    """
    client = batch_v1.BatchServiceClient()

    return client.delete_job(name=f"projects/{project_id}/locations/{region}/jobs/{job_name}")
# [END batch_delete_job]
