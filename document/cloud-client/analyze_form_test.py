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
# See the License for the specific ladnguage governing permissions and
# limitations under the License.

import os
import analyze_form

PROJECT_ID = os.environ["GCLOUD_PROJECT"]
INPUT_URI = "gs://dai-pdfs/form.pdf"


def test_analyze_form():
    document = analyze_form.analyze_form(PROJECT_ID, INPUT_URI)
    assert document
    assert document.pages
    assert document.pages[0].form_fields


def test_parse_form_response():
    data = analyze_form.parse_form_response(
        analyze_form.analyze_form(PROJECT_ID, INPUT_URI))
    assert len(data)
    datum = data[0]
    assert 'name' in datum
    assert 'text' in datum['name']
    assert 'start_index' in datum['name']
    assert 'end_index' in datum['name']
    assert 'confidence' in datum['name']
    assert 'bounding_poly' in datum['name']
    assert len(datum['name']['bounding_poly']) == 8
