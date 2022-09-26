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

from samples.snippets import list_processor_versions_sample

location = "us"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
processor_id = "52a38e080c1a7296"


def test_list_processor_versions(capsys):
    list_processor_versions_sample.list_processor_versions_sample(
        project_id=project_id, location=location, processor_id=processor_id
    )
    out, _ = capsys.readouterr()

    assert "Processor Version: pretrained-ocr" in out
    assert "Display Name: Google Stable" in out
    assert "Display Name: Google Release Candidate" in out
    assert "DEPLOYED" in out
