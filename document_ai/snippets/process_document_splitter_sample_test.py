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

from samples.snippets import process_document_splitter_sample


location = "us"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
processor_id = "ed55eeb2b276066f"
file_path = "resources/multi_document.pdf"


def test_process_documents(capsys):
    process_document_splitter_sample.process_document_splitter_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        file_path=file_path,
    )
    out, _ = capsys.readouterr()

    expected_strings = [
        "Found 8 subdocuments",
        "confident that pages 1 to 2 are a subdocument",
        "confident that page 10 is a subdocument",
    ]
    for expected_string in expected_strings:
        assert expected_string in out
