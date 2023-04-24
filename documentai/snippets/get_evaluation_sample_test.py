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

import os
from unittest import mock

from documentai.snippets import get_evaluation_sample


location = "us"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
processor_id = "a35310a144a6e4f8"
processor_version_id = "2af620b2fd4d1fcf"
evaluation_id = "55cdab6206095055"


# Mocking request
@mock.patch("google.cloud.documentai.DocumentProcessorServiceClient.get_evaluation")
@mock.patch("google.cloud.documentai.Evaluation")
def test_get_evaluation(evaluation_mock, get_evaluation_mock, capsys):
    get_evaluation_mock.return_value = evaluation_mock

    get_evaluation_sample.get_evaluation_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        processor_version_id=processor_version_id,
        evaluation_id=evaluation_id,
    )

    get_evaluation_mock.assert_called_once()

    out, _ = capsys.readouterr()

    assert "Create Time" in out
