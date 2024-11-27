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

# [START genappbuilder_train_custom_model]

from google.api_core.client_options import ClientOptions
from google.api_core.operation import Operation
from google.cloud import discoveryengine

# TODO(developer): Uncomment these variables before running the sample.
# project_id = "YOUR_PROJECT_ID"
# location = "YOUR_LOCATION" # Values: "global"
# data_store_id = "YOUR_DATA_STORE_ID"
# corpus_data_path = "gs://my-bucket/corpus.jsonl"
# query_data_path = "gs://my-bucket/query.jsonl"
# train_data_path = "gs://my-bucket/train.tsv"
# test_data_path = "gs://my-bucket/test.tsv"


def train_custom_model_sample(
    project_id: str,
    location: str,
    data_store_id: str,
    corpus_data_path: str,
    query_data_path: str,
    train_data_path: str,
    test_data_path: str,
) -> Operation:
    #  For more information, refer to:
    # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )
    # Create a client
    client = discoveryengine.SearchTuningServiceClient(client_options=client_options)

    # The full resource name of the data store
    data_store = f"projects/{project_id}/locations/{location}/collections/default_collection/dataStores/{data_store_id}"

    # Make the request
    operation = client.train_custom_model(
        request=discoveryengine.TrainCustomModelRequest(
            gcs_training_input=discoveryengine.TrainCustomModelRequest.GcsTrainingInput(
                corpus_data_path=corpus_data_path,
                query_data_path=query_data_path,
                train_data_path=train_data_path,
                test_data_path=test_data_path,
            ),
            data_store=data_store,
            model_type="search-tuning",
        )
    )

    # Optional: Wait for training to complete
    # print(f"Waiting for operation to complete: {operation.operation.name}")
    # response = operation.result()

    # After the operation is complete,
    # get information from operation metadata
    # metadata = discoveryengine.TrainCustomModelMetadata(operation.metadata)

    # Handle the response
    # print(response)
    # print(metadata)
    print(operation)

    return operation


# [END genappbuilder_train_custom_model]
