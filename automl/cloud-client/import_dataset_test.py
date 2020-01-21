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

import datetime
import os

from google.cloud import automl
import pytest

import import_dataset

PROJECT_ID = os.environ["AUTOML_PROJECT_ID"]
BUCKET_ID = "{}-lcm".format(PROJECT_ID)


@pytest.fixture(scope="function")
def dataset_id():
    client = automl.AutoMlClient()
    project_location = client.location_path(PROJECT_ID, "us-central1")
    display_name = "test_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    metadata = automl.types.TextSentimentDatasetMetadata(
        sentiment_max=4
    )
    dataset = automl.types.Dataset(
        display_name=display_name, text_sentiment_dataset_metadata=metadata
    )
    response = client.create_dataset(project_location, dataset)
    dataset_id = response.result().name.split("/")[-1]

    yield dataset_id


@pytest.mark.slow
def test_import_dataset(capsys, dataset_id):
    # Importing a dataset can take a long time and only four operations can be
    # run on a project at once. Try to import the dataset and if a resource
    # exhausted error is thrown, catch it. Otherwise, proceed as usual.
    try:
        data = (
            "gs://{}/sentiment-analysis/dataset.csv".format(BUCKET_ID)
        )
        created_dataset_id = dataset_id
        import_dataset.import_dataset(PROJECT_ID, created_dataset_id, data)
        out, _ = capsys.readouterr()
        assert "Data imported." in out
    except Exception as e:
        assert (
                "ResourceExhausted: 429 There are too many import data "
                "operations are running in parallel"
                in e.message
        )

    # delete created dataset
    client = automl.AutoMlClient()
    dataset_full_id = client.dataset_path(
        PROJECT_ID, "us-central1", created_dataset_id
    )
    response = client.delete_dataset(dataset_full_id)
    response.result()


