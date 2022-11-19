# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os

import translate_v3beta1_translate_document

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]

FILE_PATH = "resources/fake_invoice.pdf"


def test_translate_document(capsys):
    translate_v3beta1_translate_document.translate_document(project_id=PROJECT_ID, file_path=FILE_PATH)
    out, _ = capsys.readouterr()
    assert "Response" in out
