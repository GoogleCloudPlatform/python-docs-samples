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

from google.cloud import automl
import pytest

import language_sentiment_analysis_create_model

PROJECT_ID = os.environ["AUTOML_PROJECT_ID"]
DATASET_ID = os.environ["SENTIMENT_ANALYSIS_DATASET_ID"]


@pytest.mark.slow
def test_sentiment_analysis_create_model(capsys):
    language_sentiment_analysis_create_model.create_model(
        PROJECT_ID, DATASET_ID, "sentiment_test_create_model"
    )
    out, _ = capsys.readouterr()
    assert "Training started" in out

    # Cancel the operation
    operation_id = out.split("Training operation name: ")[1].split("\n")[0]
    client = automl.AutoMlClient()
    client.transport._operations_client.cancel_operation(operation_id)
