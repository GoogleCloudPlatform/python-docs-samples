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

from documentai.snippets import process_document_sample

location = "us"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
processor_id = "90484cfdedb024f6"
file_path = "resources/invoice.pdf"
mime_type = "application/pdf"
field_mask = "text,pages.pageNumber"


def test_process_documents(capsys):
    process_document_sample.process_document_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        file_path=file_path,
        mime_type=mime_type,
        field_mask=field_mask,
    )
    out, _ = capsys.readouterr()

    assert "text:" in out
    assert "Invoice" in out
