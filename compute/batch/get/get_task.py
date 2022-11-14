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

# [START batch_get_task]

from google.cloud import batch_v1


def get_task(project_id: str, region: str, job_name: str, group_name: str, task_number: int) -> batch_v1.Task:
    """
    Retrieve information about a Task.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        region: name of the region hosts the job.
        job_name: the name of the job you want to retrieve information about.
        group_name: the name of the group that owns the task you want to check. Usually it's `group0`.
        task_number: number of the task you want to look up.

    Returns:
        A Task object representing the specified task.
    """
    client = batch_v1.BatchServiceClient()

    return client.get_task(name=f"projects/{project_id}/locations/{region}/jobs/{job_name}"
                                f"/taskGroups/{group_name}/tasks/{task_number}")
# [END batch_get_task]
