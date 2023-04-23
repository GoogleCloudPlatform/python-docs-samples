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


import re

import create_fileset_entry


def test_create_fileset_entry(capsys, client, random_entry_name):

    entry_name_pattern = "(?P<entry_group_name>.+?)/entries/(?P<entry_id>.+?$)"
    entry_name_matches = re.match(entry_name_pattern, random_entry_name)
    entry_group_name = entry_name_matches.group("entry_group_name")
    entry_id = entry_name_matches.group("entry_id")

    create_fileset_entry.create_fileset_entry(client, entry_group_name, entry_id)
    out, err = capsys.readouterr()
    assert f"Created entry {random_entry_name}" in out
