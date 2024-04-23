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
from typing import Dict, List, Union

import google.auth
from google.iam.v1 import policy_pb2
import pytest
from snippets.get_policy import get_policy
from snippets.set_policy import set_policy

PROJECT = google.auth.default()[1]


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
