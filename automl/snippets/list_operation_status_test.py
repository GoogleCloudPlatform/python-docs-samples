# Copyright 2020 Google LLC
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

import os

import backoff
from google.api_core.exceptions import InternalServerError
import pytest

import list_operation_status

PROJECT_ID = os.environ["AUTOML_PROJECT_ID"]


@pytest.mark.slow
def test_list_operation_status(capsys):
    # We saw 500 InternalServerError. Now we just retry few times.
    @backoff.on_exception(backoff.expo, InternalServerError, max_time=120)
    def run_sample():
        list_operation_status.list_operation_status(PROJECT_ID)

    run_sample()
    out, _ = capsys.readouterr()
    assert "Operation details" in out
