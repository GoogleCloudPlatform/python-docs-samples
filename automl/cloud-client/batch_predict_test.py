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

import datetime
import os

from google.cloud import automl
from google.cloud import storage
import pytest

import batch_predict

PROJECT_ID = os.environ["GCLOUD_PROJECT"]
BUCKET_ID = "{}-lcm".format(PROJECT_ID)
MODEL_ID = "TEN5112482778553778176"
PREFIX = "TEST_EXPORT_OUTPUT_" + datetime.datetime.now().strftime(
    "%Y%m%d%H%M%S"
)


@pytest.fixture(scope="function")
def verify_model_state():
    client = automl.AutoMlClient()
    model_full_id = client.model_path(PROJECT_ID, "us-central1", MODEL_ID)
    model = client.get_model(model_full_id)
    if model.deployment_state == automl.enums.Model.DeploymentState.UNDEPLOYED:
        # Deploy model if it is not deployed
        response = client.deploy_model(model_full_id)
        response.result()


@pytest.mark.slow
def test_batch_predict(capsys, verify_model_state):
    verify_model_state
    input_uri = "gs://{}/entity_extraction/input.jsonl".format(BUCKET_ID)
    output_uri = "gs://{}/{}/".format(BUCKET_ID, PREFIX)
    batch_predict.batch_predict(PROJECT_ID, MODEL_ID, input_uri, output_uri)
    out, _ = capsys.readouterr()
    assert "Batch Prediction results saved to Cloud Storage bucket" in out

    # Delete created files
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_ID)
    if len(list(bucket.list_blobs(prefix=PREFIX))) > 0:
        for blob in bucket.list_blobs(prefix=PREFIX):
            blob.delete()
