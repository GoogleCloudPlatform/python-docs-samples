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
from uuid import uuid4

from documentai.snippets import quickstart_sample

from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1

from google.cloud.documentai_v1.types.processor import Processor

import pytest

LOCATION = "us"
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
FILE_PATH = "resources/invoice.pdf"


@pytest.fixture(scope="module")
def client() -> documentai_v1.DocumentProcessorServiceClient:
    opts = ClientOptions(api_endpoint=f"{LOCATION}-documentai.googleapis.com")

    client = documentai_v1.DocumentProcessorServiceClient(client_options=opts)

    return client


@pytest.fixture(scope="module")
def processor_id(client: documentai_v1.DocumentProcessorServiceClient) -> Processor:
    processor_display_name = f"test-processor-{uuid4()}"

    # Get the full resource name of the location.
    # For example: `projects/{project_id}/locations/{location}`
    parent = client.common_location_path(PROJECT_ID, LOCATION)

    # Create a Processor.
    # https://cloud.google.com/document-ai/docs/create-processor#available_processors
    processor = client.create_processor(
        parent=parent,
        processor=documentai_v1.Processor(
            type_="OCR_PROCESSOR",
            display_name=processor_display_name,
        ),
    )

    # `processor.name` (Full Processor Path) has this form:
    # `projects/{project_id}/locations/{location}/processors/{processor_id}`
    # Return only the `processor_id` section.
    last_slash_index = processor.name.rfind('/')
    yield processor.name[last_slash_index + 1:]

    # Delete processor.
    client = documentai_v1.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{LOCATION}-documentai.googleapis.com"
        )
    )
    client.delete_processor(name=processor.name)


def test_quickstart(processor_id: str) -> None:
    document = quickstart_sample.quickstart(
        project_id=PROJECT_ID,
        processor_id=processor_id,
        location=LOCATION,
        file_path=FILE_PATH,
    )

    assert "Invoice" in document.text
