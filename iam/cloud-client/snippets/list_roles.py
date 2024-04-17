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

# [START iam_list_roles]
from google.cloud.iam_admin_v1 import (
    IAMClient,
    RoleView,
)
from google.cloud.iam_admin_v1.services.iam.pagers import ListRolesPager


def list_roles(
    project_id: str, show_deleted: bool = True, role_view: RoleView = RoleView.BASIC
) -> ListRolesPager:
    client = IAMClient()
    parent = f"projects/{project_id}"
    request = {
        "parent": parent,
        "view": role_view,
        "show_deleted": show_deleted,
    }
    roles = client.list_roles(request)
    for page in roles.pages:
        for role in page.roles:
            print(role)
    print("Listed all iam roles")
    return roles
# [END iam_list_roles]


if __name__ == "__main__":
    import os

    PROJECT_ID = os.environ["IAM_PROJECT_ID"]
    list_roles(PROJECT_ID)
