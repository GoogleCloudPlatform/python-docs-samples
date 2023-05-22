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

from documentai.snippets import get_operation_sample

location = "us"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
operation_id = "10828996427112056798"
operation_name = f"projects/{project_id}/locations/{location}/operations/{operation_id}"


def test_get_operation(capsys):
    get_operation_sample.get_operation_sample(
        location=location, operation_name=operation_name
    )
    out, _ = capsys.readouterr()

    assert "operation" in out
