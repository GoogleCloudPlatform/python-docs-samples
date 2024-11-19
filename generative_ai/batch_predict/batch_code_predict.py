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
from google.cloud.aiplatform import BatchPredictionJob


def batch_code_prediction(
    input_uri: str = None, output_uri: str = None
) -> BatchPredictionJob:
    """Perform batch code prediction using a pre-trained code generation model.
    Args:
        input_uri (str, optional): URI of the input dataset. Could be a BigQuery table or a Google Cloud Storage file.
            E.g. "gs://[BUCKET]/[DATASET].jsonl" OR "bq://[PROJECT].[DATASET].[TABLE]"
        output_uri (str, optional): URI where the output will be stored.
            Could be a BigQuery table or a Google Cloud Storage file.
            E.g. "gs://[BUCKET]/[OUTPUT].jsonl" OR "bq://[PROJECT].[DATASET].[TABLE]"
    Returns:
        batch_prediction_job: The batch prediction job object containing details of the job.
    """

    # [START generativeaionvertexai_batch_code_predict]
    from vertexai.preview.language_models import CodeGenerationModel

    # Example of using Google Cloud Storage bucket as the input and output data source
    # TODO (Developer): Replace the input_uri and output_uri with your own GCS paths
    # input_uri = "gs://cloud-samples-data/batch/prompt_for_batch_code_predict.jsonl"
    # output_uri = "gs://your-bucket-name/batch_code_predict_output"

    code_model = CodeGenerationModel.from_pretrained("code-bison")

    batch_prediction_job = code_model.batch_predict(
        dataset=input_uri,
        destination_uri_prefix=output_uri,
        # Optional:
        model_parameters={
            "maxOutputTokens": "200",
            "temperature": "0.2",
        },
    )
    print(batch_prediction_job.display_name)
    print(batch_prediction_job.resource_name)
    print(batch_prediction_job.state)

    # [END generativeaionvertexai_batch_code_predict]

    return batch_prediction_job


if __name__ == "__main__":
    batch_code_prediction()
