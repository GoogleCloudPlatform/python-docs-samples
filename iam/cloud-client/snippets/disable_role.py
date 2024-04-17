#!/usr/bin/env python

# Copyright 2024 Google Inc. All Rights Reserved.
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

# [START iam_disable_role]
from google.cloud.iam_admin_v1 import (
    IAMClient,
    Role,
)
from google.api_core.exceptions import NotFound


def disable_role(project_id: str, role_id: str) -> Role:
    client = IAMClient()
    name = f"projects/{project_id}/roles/{role_id}"
    request = {
        "name": name,
    }
    try:
        role = client.get_role(request)
        role.stage = Role.RoleLaunchStage.DISABLED
        request = {
            "name": role.name,
            "role": role,
        }
        client.update_role(request)
        print(f"Disabled role: {role_id}: {role}")
        return role
    except NotFound:
        raise f"Role with id [{role_id}] not found, take some actions"
# [END iam_disable_role]


if __name__ == "__main__":
    import os

    PROJECT_ID = os.environ["IAM_PROJECT_ID"]
    role_id = "custom1_python"
    disable_role(PROJECT_ID, role_id)
