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

# [START iam_create_role]
from typing import List
from google.api_core.exceptions import AlreadyExists, FailedPrecondition

from google.cloud.iam_admin_v1 import (
    IAMClient,
    Role,
)


def create_role(
    project_id: str, role_id: str, permissions: List[str], title: str | None = None
) -> Role:
    client = IAMClient()

    parent = f"projects/{project_id}"

    role = Role()
    request = {
        "parent": parent,
        "role_id": role_id,
        "role": {
            "title": title,
            "included_permissions": permissions,
        },
    }
    try:
        role = client.create_role(request)
        print(f"Created iam role: {role_id}: {role}")
        return role
    except AlreadyExists:
        print(f"Role with id [{role_id}] already exists, take some actions")
    except FailedPrecondition:
        print(
            f"Role with id [{role_id}] already exists and in deleted state, take some actions"
        )
# [END iam_create_role]


if __name__ == "__main__":
    import os

    PROJECT_ID = os.environ["IAM_PROJECT_ID"]
    role_id = "custom1_python"
    permissions = ["iam.roles.get", "iam.roles.list"]
    title = "custom1_python_title"
    create_role(PROJECT_ID, role_id, permissions, title)
