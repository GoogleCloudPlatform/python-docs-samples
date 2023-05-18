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
from unittest import mock

from documentai.snippets import evaluate_processor_version_sample

location = "us"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
processor_id = "aaaaaaaaa"
processor_version_id = "xxxxxxxxxx"
gcs_input_uri = "gs://bucket/directory/"


# Mocking request as evaluation can take a long time
@mock.patch(
    "google.cloud.documentai.DocumentProcessorServiceClient.evaluate_processor_version"
)
@mock.patch("google.cloud.documentai.EvaluateProcessorVersionResponse")
@mock.patch("google.api_core.operation.Operation")
def test_evaluate_processor_version(
    operation_mock,
    evaluate_processor_version_response_mock,
    evaluate_processor_version_mock,
    capsys,
):
    operation_mock.result.return_value = evaluate_processor_version_response_mock
    evaluate_processor_version_mock.return_value = operation_mock

    evaluate_processor_version_sample.evaluate_processor_version_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        processor_version_id=processor_version_id,
        gcs_input_uri=gcs_input_uri,
    )

    evaluate_processor_version_mock.assert_called_once()

    out, _ = capsys.readouterr()

    assert "operation" in out
