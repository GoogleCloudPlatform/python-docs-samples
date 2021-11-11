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

import quickstart


def test_quickstart(
    capsys, client, project_id, dataset_id, table_id, random_tag_template_id
):
    location = "us-central1"
    override_values = {
        "project_id": project_id,
        "dataset_id": dataset_id,
        "table_id": table_id,
        "tag_template_id": random_tag_template_id,
    }
    tag_template_name = client.tag_template_path(
        project_id, location, random_tag_template_id
    )
    quickstart.quickstart(override_values)
    out, err = capsys.readouterr()
    assert "Created template: {}".format(tag_template_name) in out
    assert "Created tag:" in out
    client.delete_tag_template(name=tag_template_name, force=True)
