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

from samples.snippets import fetch_processor_types_sample

location = "us"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]


def test_fetch_processor_types(capsys):
    fetch_processor_types_sample.fetch_processor_types_sample(
        project_id=project_id, location=location
    )
    out, _ = capsys.readouterr()

    assert "OCR_PROCESSOR" in out
    assert "FORM_PARSER_PROCESSOR" in out
