# # Copyright 2020 Google LLC
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
from uuid import uuid4

from documentai.snippets import quickstart_sample

from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore

location = "us"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
processor_display_name = f"test-processor-{uuid4()}"
file_path = "resources/invoice.pdf"


def test_quickstart(capsys):
    processor = quickstart_sample.quickstart(
        project_id=project_id,
        location=location,
        processor_display_name=processor_display_name,
        file_path=file_path,
    )
    out, _ = capsys.readouterr()

    # Delete created processor
    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-documentai.googleapis.com"
        )
    )
    operation = client.delete_processor(name=processor.name)
    # Wait for operation to complete
    operation.result()

    assert "Processor Name:" in out
    assert "text:" in out
    assert "Invoice" in out
