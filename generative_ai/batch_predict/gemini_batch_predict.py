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

from vertexai.preview.batch_prediction import BatchPredictionJob

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def batch_predict_gemini_createjob(
    input_uri: str, output_uri: str
) -> BatchPredictionJob:
    """Perform batch text prediction using a Gemini AI model.
    Args:
        input_uri (str): URI of the input file in BigQuery table or Google Cloud Storage.
            Example: "gs://[BUCKET]/[DATASET].jsonl" OR "bq://[PROJECT].[DATASET].[TABLE]"

        output_uri (str): URI of the output folder,  in BigQuery table or Google Cloud Storage.
            Example: "gs://[BUCKET]/[OUTPUT].jsonl" OR "bq://[PROJECT].[DATASET].[TABLE]"
    Returns:
        batch_prediction_job: The batch prediction job object containing details of the job.
    """

    # [START generativeaionvertexai_batch_predict_gemini_createjob]
    import time
    import vertexai

    from vertexai.preview.batch_prediction import BatchPredictionJob

    # TODO(developer): Update and un-comment below lines
    # input_uri ="gs://[BUCKET]/[OUTPUT].jsonl" # Example
    # output_uri ="gs://[BUCKET]"

    # Initialize vertexai
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # Submit a batch prediction job with Gemini model
    batch_prediction_job = BatchPredictionJob.submit(
        source_model="gemini-1.5-flash-002",
        input_dataset=input_uri,
        output_uri_prefix=output_uri,
    )

    # Check job status
    print(f"Job resource name: {batch_prediction_job.resource_name}")
    print(f"Model resource name with the job: {batch_prediction_job.model_name}")
    print(f"Job state: {batch_prediction_job.state.name}")

    # Refresh the job until complete
    while not batch_prediction_job.has_ended:
        time.sleep(5)
        batch_prediction_job.refresh()

    # Check if the job succeeds
    if batch_prediction_job.has_succeeded:
        print("Job succeeded!")
    else:
        print(f"Job failed: {batch_prediction_job.error}")

    # Check the location of the output
    print(f"Job output location: {batch_prediction_job.output_location}")

    # Example response:
    #  Job output location: gs://your-bucket/gen-ai-batch-prediction/prediction-model-year-month-day-hour:minute:second.12345

    # https://storage.googleapis.com/cloud-samples-data/batch/prompt_for_batch_gemini_predict.jsonl

    return batch_prediction_job

    # [END generativeaionvertexai_batch_predict_gemini_createjob]


if __name__ == "__main__":
    # TODO(developer): Update your Cloud Storage bucket and uri file paths
    GCS_BUCKET = "gs://your-bucket"
    batch_predict_gemini_createjob(
        input_uri=f"gs://{GCS_BUCKET}/batch_data/sample_input_file.jsonl",
        output_uri=f"gs://{GCS_BUCKET}/batch_predictions/sample_output/",
    )
