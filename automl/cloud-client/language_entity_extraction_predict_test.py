#!/usr/bin/env python

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

import os

import language_entity_extraction_predict

PROJECT_ID = os.environ["GCLOUD_PROJECT"]
BUCKET_ID = "{}-lcm".format(PROJECT_ID)


def test_predict(capsys):
    model_id = "TEN5112482778553778176"
    text = (
        "Constitutional mutations in the WT1 gene in patients with "
        "Denys-Drash syndrome."
    )
    language_entity_extraction_predict.predict(PROJECT_ID, model_id, text)
    out, _ = capsys.readouterr()
    assert "Text Extract Entity Types: " in out
