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
from documentai.snippets import delete_processor_version_sample
from documentai.snippets import list_processor_versions_sample
from documentai.snippets import get_processor_version_sample

import mock

location = "us"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
processor_id = "aadcbbfe0db33e46"
train_data_uri = "gs://document-ai-workbench-python-integration/train_test_data/"
test_data_uri = train_data_uri


class EphemeralProcessorFixture:
    def __init__(self, processor_version_display_name):
        self.processor_version_display_name = processor_version_display_name
        self.processor_version = None

    def teardown(self):
        if not self.processor_version:

            processor_versions = (
                list_processor_versions_sample.list_processor_versions_sample(
                    project_id=project_id, location=location, processor_id=processor_id
                )
            )

            for processor_version in processor_versions:
                if (
                    processor_version.display_name
                    == self.processor_version_display_name
                ):
                    self.processor_version = processor_version.name.split("/")[-1]

        while True:
            processor_version = (
                get_processor_version_sample.get_processor_version_sample(
                    project_id=project_id,
                    location=location,
                    processor_id=processor_id,
                    processor_version_id=self.processor_version,
                )
            )

            if processor_version.state != processor_version.state.CREATING:
                break

        delete_processor_version_sample.delete_processor_version_sample(
            project_id=project_id,
            location=location,
            processor_id=processor_id,
            processor_version_id=self.processor_version,
        )


@pytest.fixture(scope="function")
def ephemeral_processor_fixture():
    _ephemeral_processor_fixture = EphemeralProcessorFixture(
        f"new-processor-version-{uuid.uuid4()}"
    )
    try:
        yield _ephemeral_processor_fixture
    except Exception as e:
        pass

    _ephemeral_processor_fixture.teardown()


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
def test_train_processor_version_integration(ephemeral_processor_fixture):

    response = train_processor_version_sample.train_processor_version_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        processor_version_display_name=ephemeral_processor_fixture.processor_version_display_name,
        train_data_uri=train_data_uri,
        test_data_uri=test_data_uri,
    )

    # Populate attribute for teardown
    ephemeral_processor_fixture.processor_version = response.processor_version
