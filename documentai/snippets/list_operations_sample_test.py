# Copyright 2022 Google LLC
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
#

# flake8: noqa

import os

from documentai.snippets import list_operations_sample

location = "us"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
operations_filter = "TYPE=BATCH_PROCESS_DOCUMENTS AND STATE=DONE"


def test_list_operations(capsys):
    list_operations_sample.list_operations_sample(
        project_id=project_id, location=location, operations_filter=operations_filter
    )
    out, _ = capsys.readouterr()

    assert "operations" in out
