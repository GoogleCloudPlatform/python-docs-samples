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

import os

from documentai.snippets import process_document_form_sample

location = "us"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
processor_id = "90484cfdedb024f6"
file_path = "resources/invoice.pdf"
mime_type = "application/pdf"


def test_process_documents(capsys):
    process_document_form_sample.process_document_form_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        file_path=file_path,
        mime_type=mime_type,
    )
    out, _ = capsys.readouterr()

    expected_strings = [
        "There are 1 page(s) in this document.",
        "Table with 4 columns and 6 rows",
        "Found 13 form field(s)",
        "'BALANCE DUE': '$2140.00'",
    ]
    for expected_string in expected_strings:
        assert expected_string in out
