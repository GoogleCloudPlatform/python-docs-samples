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
import uuid

from google.cloud import automl_v1beta1 as automl
import pytest

import video_object_tracking_create_model

PROJECT_ID = os.environ["GCLOUD_PROJECT"]
DATASET_ID = "VOT2823376535338090496"
OPERATION_ID = None


@pytest.fixture(scope="function", autouse=True)
def teardown():
    yield

    # Cancel the training operation
    client = automl.AutoMlClient()
    client.transport._operations_client.cancel_operation(OPERATION_ID)


def test_video_classification_create_model(capsys):
    model_name = "test_{}".format(uuid.uuid4()).replace("-", "")[:32]
    video_object_tracking_create_model.create_model(
        PROJECT_ID, DATASET_ID, model_name
    )
    out, _ = capsys.readouterr()
    assert "Training started" in out

    # Cancel the operation
    global OPERATION_ID
    OPERATION_ID = out.split("Training operation name: ")[1].split("\n")[0]
