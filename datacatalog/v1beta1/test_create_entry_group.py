# Copyright 2019 Google LLC
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


import create_entry_group


def test_create_entry_group(capsys, client, project_id, random_entry_group_id):

    create_entry_group.create_entry_group(project_id, random_entry_group_id)
    out, err = capsys.readouterr()
    assert (
        "Created entry group"
        " projects/{}/locations/{}/entryGroups/{}".format(
            project_id, "us-central1", random_entry_group_id
        )
        in out
    )
