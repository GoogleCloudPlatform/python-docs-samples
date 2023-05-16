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
from uuid import uuid4

from documentai.snippets import create_processor_sample

location = "us"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
processor_display_name = f"test-processor-{uuid4()}"
processor_type = "OCR_PROCESSOR"


@mock.patch("google.cloud.documentai.DocumentProcessorServiceClient.create_processor")
@mock.patch("google.cloud.documentai.Processor")
def test_create_processor(create_processor_mock, processor_mock, capsys):
    create_processor_mock.return_value = processor_mock

    create_processor_sample.create_processor_sample(
        project_id=project_id,
        location=location,
        processor_display_name=processor_display_name,
        processor_type=processor_type,
    )

    create_processor_mock.assert_called_once()

    out, _ = capsys.readouterr()

    assert "Processor Name:" in out
    assert "Processor Display Name:" in out
    assert "Processor Type:" in out
