# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import create_fileset


def test_create_fileset(
    capsys,
    client,
    project_id,
    random_entry_group_id,
    random_entry_id,
    resources_to_delete,
):
    location = "us-central1"
    override_values = {
        "project_id": project_id,
        "fileset_entry_group_id": random_entry_group_id,
        "fileset_entry_id": random_entry_id,
    }
    expected_group_name = client.entry_group_path(
        project_id, location, random_entry_group_id
    )
    expected_entry_name = client.entry_path(
        project_id, location, random_entry_group_id, random_entry_id
    )
    create_fileset.create_fileset(override_values)
    out, err = capsys.readouterr()
    assert f"Created entry group: {expected_group_name}" in out
    assert f"Created fileset entry: {expected_entry_name}" in out
    resources_to_delete["entry_groups"].append(expected_group_name)
    resources_to_delete["entries"].append(expected_entry_name)
