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

# [START batch_list_tasks]
from typing import Iterable

from google.cloud import batch_v1


def list_tasks(project_id: str, region: str, job_name: str, group_name: str) -> Iterable[batch_v1.Task]:
    """
    Get a list of all jobs defined in given region.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        region: name of the region hosting the jobs.
        job_name: name of the job which tasks you want to list.
        group_name: name of the group of tasks. Usually it's `group0`.

    Returns:
        An iterable collection of Task objects.
    """
    client = batch_v1.BatchServiceClient()

    return client.list_tasks(parent=f"projects/{project_id}/locations/{region}/jobs/{job_name}/taskGroups/{group_name}")
# [END batch_list_tasks]
