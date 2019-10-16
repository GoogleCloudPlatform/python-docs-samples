# Copyright 2019 Google LLC
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
import pytest
import uuid
import translate_v3_translate_text_with_model

PROJECT_ID = os.environ['GCLOUD_PROJECT']
MODEL_ID = os.environ['AUTOML_TRANSLATION_MODEL_ID']

def test_translate_text_with_model(capsys):
    translate_v3_translate_text_with_model.sample_translate_text_with_model(
        MODEL_ID,
        "That' il do it.",
        "ja",
        "en",
        PROJECT_ID,
        "us-central1")
    out, _ = capsys.readouterr()
    assert 'それはそうだ' in out
