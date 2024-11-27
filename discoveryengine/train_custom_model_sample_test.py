# Copyright 2024 Google LLC
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
#

import os

from discoveryengine import train_custom_model_sample
from google.api_core.exceptions import AlreadyExists

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "global"
data_store_id = "tuning-data-store"
corpus_data_path = "gs://cloud-samples-data/gen-app-builder/search-tuning/corpus.jsonl"
query_data_path = "gs://cloud-samples-data/gen-app-builder/search-tuning/query.jsonl"
train_data_path = "gs://cloud-samples-data/gen-app-builder/search-tuning/training.tsv"
test_data_path = "gs://cloud-samples-data/gen-app-builder/search-tuning/test.tsv"


def test_train_custom_model():
    try:
        operation = train_custom_model_sample.train_custom_model_sample(
            project_id,
            location,
            data_store_id,
            corpus_data_path,
            query_data_path,
            train_data_path,
            test_data_path,
        )
        assert operation
    except AlreadyExists:
        # Ignore AlreadyExists; training is already in progress.
        pass
