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
#

# flake8: noqa

import os

from documentai.snippets import process_document_specialized_sample

location = "us"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
processor_id = "feacd98c28866ede"
file_path = "resources/us_driver_license.pdf"
mime_type = "application/pdf"


def test_process_documents(capsys):
    process_document_specialized_sample.process_document_specialized_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        file_path=file_path,
        mime_type=mime_type,
    )
    out, _ = capsys.readouterr()

    expected_strings = [
        "Document Id",
        "97551579",
    ]
    for expected_string in expected_strings:
        assert expected_string in out
