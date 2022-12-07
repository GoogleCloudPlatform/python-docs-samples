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


# [START automl_batch_predict_beta]
from google.cloud import automl_v1beta1 as automl


def batch_predict(
    project_id="YOUR_PROJECT_ID",
    model_id="YOUR_MODEL_ID",
    input_uri="gs://YOUR_BUCKET_ID/path/to/your/input/csv_or_jsonl",
    output_uri="gs://YOUR_BUCKET_ID/path/to/save/results/",
):
    """Batch predict"""
    prediction_client = automl.PredictionServiceClient()

    # Get the full path of the model.
    model_full_id = automl.AutoMlClient.model_path(
        project_id, "us-central1", model_id
    )

    gcs_source = automl.GcsSource(input_uris=[input_uri])

    input_config = automl.BatchPredictInputConfig(gcs_source=gcs_source)
    gcs_destination = automl.GcsDestination(output_uri_prefix=output_uri)
    output_config = automl.BatchPredictOutputConfig(
        gcs_destination=gcs_destination
    )
    params = {}

    request = automl.BatchPredictRequest(
        name=model_full_id,
        input_config=input_config,
        output_config=output_config,
        params=params
    )
    response = prediction_client.batch_predict(
        request=request
    )

    print("Waiting for operation to complete...")
    print(
        "Batch Prediction results saved to Cloud Storage bucket. {}".format(
            response.result()
        )
    )
# [END automl_batch_predict_beta]
