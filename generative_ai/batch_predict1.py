# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

import vertexai

from vertexai.preview.language_models import TextGenerationModel

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
DATASET_ID = "123test"


# [START aiplatform_batch_predict]


def batch_prediction(input_uri: str = None, output_uri: str = None):
    vertexai.init(project=PROJECT_ID, location="us-east1")
    try:
        public_model = "gemini-pro"
        print("Trying to load model", public_model)
        my_model = TextGenerationModel.from_pretrained(public_model)
        print(my_model)
    except Exception as e:
        print(e)
        print("Model not found")

    try:
        public_model = "gemini-1.5-flash-001"
        print("Trying to load model", public_model)
        my_model = TextGenerationModel.from_pretrained(public_model)
        print(my_model)
    except Exception as e:
        print(e)
        print("Model not found")

    try:
        public_model = "gemini-1.0-pro-002"
        print("Trying to load model", public_model)
        my_model = TextGenerationModel.from_pretrained(public_model)
        print(my_model)
    except Exception as e:
        print(e)
        print("Model not found")

    # batch_prediction_job = my_model.batch_predict(
    #     bigquery_source=f"bq://{PROJECT_ID}.{DATASET_ID}.batch_requests",
    #     bigquery_destination_prefix=f"bq://{PROJECT_ID}.{DATASET_ID}.ready_requests3",
    #     model_parameters={
    #         "maxOutputTokens": 200,
    #         "temperature": 0.2,
    #         "topP": 0.95,
    #         "topK": 40,
    #     },
    # )

    # text_model = TextGenerationModel.from_pretrained(model_name=f"projects/{PROJECT_ID}/locations/us-central1/models/gemini-1.0-pro-002")
    # batch_prediction_job = text_model.batch_predict(
    #     dataset=f"bq://{PROJECT_ID}.{DATASET_ID}.batch_requests",
    #     destination_uri_prefix=f"bq://{PROJECT_ID}.{DATASET_ID}.ready_requests",
    #     # Optional:
    #     model_parameters={
    #         "maxOutputTokens": "200",
    #         "temperature": "0.2",
    #         "topP": "0.95",
    #         "topK": "40",
    #     },
    # )

    # print(batch_prediction_job.display_name)
    # print(batch_prediction_job.resource_name)
    # print(batch_prediction_job.state)


# [END aiplatform_batch_predict]
if __name__ == "__main__":
    a = batch_prediction()
    print(a)
