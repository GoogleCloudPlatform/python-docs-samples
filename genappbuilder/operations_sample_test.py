# Copyright 2023 Google LLC
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

import os

from genappbuilder import get_operation_sample
from genappbuilder import list_operations_sample
from genappbuilder import poll_operation_sample

from google.api_core.exceptions import NotFound

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "global"
search_engine_id = "test-structured-data-engine"
operation_id = "import-documents-6754238352371303556"
operation_name = f"projects/{project_id}/locations/{location}/collections/default_collection/dataStores/{search_engine_id}/branches/0/operations/{operation_id}"


def test_get_operation(capsys):
    try:
        get_operation_sample.get_operation_sample(operation_name=operation_name)
    except NotFound as e:
        print(e.message)

    out, _ = capsys.readouterr()

    assert operation_id in out


def test_poll_operation(capsys):
    try:
        poll_operation_sample.poll_operation_sample(operation_name=operation_name)
    except NotFound as e:
        print(e.message)

    out, _ = capsys.readouterr()

    assert operation_id in out
