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

import pytest

import os
import uuid

from documentai.snippets import train_processor_version_sample

import mock

location = "us"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
processor_id = "aadcbbfe0db33e46"
train_data_uri = "gs://document-ai-workbench-python-integration/documents"
test_data_uri = train_data_uri


@pytest.fixture(scope="function")
def processor_version_display_name():
    ephemeral_processor_version_display_name = f"new-processor-version-{uuid.uuid4()}"
    yield ephemeral_processor_version_display_name, None


@mock.patch(
    "google.cloud.documentai_v1beta3.DocumentProcessorServiceClient.train_processor_version"
)
@mock.patch("google.cloud.documentai_v1beta3.TrainProcessorVersionResponse")
@mock.patch("google.cloud.documentai_v1beta3.TrainProcessorVersionMetadata")
@mock.patch("google.api_core.operation.Operation")
def test_train_processor_version(
    processor_version_display_name,
    operation_mock,
    train_processor_version_metadata_mock,
    train_processor_version_response_mock,
    train_processor_version_mock,
    capsys,
):
    operation_mock.result.return_value = train_processor_version_response_mock
    operation_mock.metadata.return_value = train_processor_version_metadata_mock
    train_processor_version_mock.return_value = operation_mock

    train_processor_version_sample.train_processor_version_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        processor_version_display_name=processor_version_display_name,
        train_data_uri=train_data_uri,
        test_data_uri=test_data_uri,
    )

    train_processor_version_mock.assert_called_once()

    out, _ = capsys.readouterr()

    assert "operation" in out


@pytest.mark.integration
def _test_train_processor_version(processor_version_display_name, capsys):

    train_processor_version_sample.train_processor_version_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        processor_version_display_name=processor_version_display_name,
        train_data_uri=train_data_uri,
        test_data_uri=test_data_uri,
    )

    out, _ = capsys.readouterr()

    assert "operation" in out
    assert "New Processor Version" in out
