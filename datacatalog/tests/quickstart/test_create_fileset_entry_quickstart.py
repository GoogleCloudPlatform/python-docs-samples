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

from google.cloud import datacatalog_v1beta1

from ...quickstart import create_fileset_entry_quickstart


def test_create_fileset_entry_quickstart(
    capsys, client, project_id, random_entry_group_id, random_entry_id
):

    create_fileset_entry_quickstart.create_fileset_entry_quickstart(
        client, project_id, random_entry_group_id, random_entry_id
    )
    out, err = capsys.readouterr()
    assert (
        "Created entry group"
        " projects/{}/locations/{}/entryGroups/{}".format(
            project_id, "us-central1", random_entry_group_id
        )
        in out
    )

    expected_entry_name = datacatalog_v1beta1.DataCatalogClient.entry_path(
        project_id, "us-central1", random_entry_group_id, random_entry_id
    )

    assert "Created entry {}".format(expected_entry_name) in out
