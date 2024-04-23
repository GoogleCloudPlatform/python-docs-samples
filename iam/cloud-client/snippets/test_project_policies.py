# Copyright 2024 Google LLC
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

from copy import deepcopy
import re
from typing import Dict, List, Union
import uuid

import google.auth
from google.iam.v1 import policy_pb2
import pytest
from snippets.create_service_account import create_service_account
from snippets.delete_service_account import delete_service_account
from snippets.get_policy import get_policy
from snippets.modify_policy_add_member import modify_policy_add_member
from snippets.set_policy import set_policy

PROJECT = google.auth.default()[1]


@pytest.fixture
def service_account(capsys: "pytest.CaptureFixture[str]") -> str:
    name = f"test-{uuid.uuid4().hex[:25]}"
    created = False
    try:
        create_service_account(PROJECT, name)
        created = True
        email = f"{name}@{PROJECT}.iam.gserviceaccount.com"
        yield email
    finally:
        if created:
            delete_service_account(PROJECT, email)
            out, _ = capsys.readouterr()
            assert re.search(f"Deleted a service account: {email}", out)


@pytest.fixture
def project_bindings() -> policy_pb2.Policy:
    try:
        policy = get_policy(PROJECT)
        bindings = format_bindings(policy)
        bindings_copy = deepcopy(bindings)
        yield bindings_copy
    finally:
        updated_policy = set_policy(PROJECT, bindings)

        assert updated_policy.etag != policy.etag
        updated_policy.ClearField("etag")
        policy.ClearField("etag")
        assert updated_policy == policy


def format_bindings(policy: policy_pb2.Policy) -> List[Dict[str, Union[str, List[str]]]]:
    bindings = []
    for bind in policy.bindings:
        binding = {"role": "", "members": []}
        # Role, which will be assigned to an entity
        binding["role"] = bind.role
        binding["members"].extend(bind.members)
        bindings.append(binding)
    return bindings


def test_set_policy(project_bindings: List[Dict[str, Union[str, List[str]]]]) -> None:
    test_binding = {"role": "roles/viewer", "members": [f"serviceAccount:{PROJECT}@appspot.gserviceaccount.com"]}
    project_bindings.append(test_binding)

    policy = set_policy(PROJECT, project_bindings)

    binding_found = False
    for bind in policy.bindings:
        if bind.role == test_binding["role"]:
            binding_found = test_binding["members"][0] in bind.members
            break
    assert binding_found


def test_modify_policy_add_member(project_bindings: List[Dict[str, Union[str, List[str]]]], service_account: str) -> None:
    role = "roles/viewer"
    test_binding = {"role": role, "members": [f"serviceAccount:{PROJECT}@appspot.gserviceaccount.com"]}
    project_bindings.append(test_binding)
    policy = set_policy(PROJECT, project_bindings)
    binding_found = False
    for bind in policy.bindings:
        if bind.role == test_binding["role"]:
            binding_found = test_binding["members"][0] in bind.members
            break
    assert binding_found

    member = f"serviceAccount:{service_account}"
    policy = modify_policy_add_member(PROJECT, project_bindings, role, member)

    binding_modified = False
    for bind in policy.bindings:
        if bind.role == test_binding["role"]:
            binding_modified = member in bind.members
            break
    assert binding_modified
