# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
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

from samples.snippets import parse_with_model_v1beta2

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
INPUT_URI = "gs://cloud-samples-data/documentai/invoice.pdf"
AUTOML_NL_MODEL_ID = "TCN3472481026502981088"

if "AUTOML_NL_MODEL_ID" in os.environ:
    AUTOML_NL_MODEL_ID = os.environ["AUTOML_NL_MODEL_ID"]

MODEL_NAME = "projects/{}/locations/us-central1/models/{}".format(
    PROJECT_ID, AUTOML_NL_MODEL_ID
)


def test_parse_with_model(capsys):
    parse_with_model_v1beta2.parse_with_model(PROJECT_ID, INPUT_URI, MODEL_NAME)
    out, _ = capsys.readouterr()
    assert "Label detected" in out
    assert "Confidence" in out
