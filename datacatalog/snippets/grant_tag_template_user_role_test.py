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


import grant_tag_template_user_role


def test_grant_tag_template_user_role(
    capsys, project_id, random_existing_tag_template_id, valid_member_id
):
    override_values = {
        "project_id": project_id,
        "tag_template_id": random_existing_tag_template_id,
        "member_id": valid_member_id,
    }
    grant_tag_template_user_role.grant_tag_template_user_role(override_values)
    out, err = capsys.readouterr()
    assert f"Member: {valid_member_id}, Role: roles/datacatalog.tagTemplateUser" in out
