# Copyright 2020 Google LLC
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

import translate_v3_get_glossary


PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
GLOSSARY_ID = "DO_NOT_DELETE_TEST_GLOSSARY"


def test_get_glossary(capsys):
    translate_v3_get_glossary.get_glossary(PROJECT_ID, GLOSSARY_ID)
    out, _ = capsys.readouterr()
    assert "gs://cloud-samples-data/translation/glossary_ja.csv" in out
