# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import backoff
from google.api_core.exceptions import InternalServerError, ServiceUnavailable

import instantiate_inline_workflow_template

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"


@backoff.on_exception(backoff.expo, (InternalServerError, ServiceUnavailable), max_tries=5)
def test_workflows(capsys):
    # Wrapper function for client library function
    instantiate_inline_workflow_template.instantiate_inline_workflow_template(
        PROJECT_ID, REGION
    )

    out, _ = capsys.readouterr()
    assert "successfully" in out
