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

LOCATION = "us"
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
PROCESSOR_DISPLAY_NAME = f"test-processor-{uuid4()}"
FILE_PATH = "resources/invoice.pdf"


def test_quickstart() -> None:
    processor, document = quickstart_sample.quickstart(
        project_id=PROJECT_ID,
        location=LOCATION,
        processor_display_name=PROCESSOR_DISPLAY_NAME,
        file_path=FILE_PATH,
    )

    assert processor is not None
    assert "Invoice" in document.text

    # Delete created processor
    client = documentai_v1.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{LOCATION}-documentai.googleapis.com"
        )
    )
    operation = client.delete_processor(name=processor.name)

    # Wait for operation to complete
    operation.result()
