# Copyright 2023 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START logging_list_logs]
from typing import List
from google.cloud import logging_v2


def list_logs(project_id: str) -> List[str]:
    """Lists all logs in a project.

    Args:
        project_id: the ID of the project

    Returns:
        A list of log names.
    """
    client = logging_v2.services.logging_service_v2.LoggingServiceV2Client()
    request = logging_v2.types.ListLogsRequest(
        parent=f"projects/{project_id}",
    )

    logs = client.list_logs(request=request)
    for log in logs:
        print(log)

    return logs


# [END logging_list_logs]
