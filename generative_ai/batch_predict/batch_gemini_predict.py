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
from email.policy import default
import os
import time

import vertexai

from typing import Optional

from vertexai.preview.batch_prediction import BatchPredictionJob

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"


def batch_gemini_prediction(
    input_uri: str = Optional[str], output_uri: str = Optional[str]
) -> BatchPredictionJob:
    """Perform batch text prediction using a Gemini AI model.
    Args:
        input_uri (str, optional): URI of the input dataset. Could be a BigQuery table or a Google Cloud Storage file.
            E.g. "gs://[BUCKET]/[DATASET].jsonl" OR "bq://[PROJECT].[DATASET].[TABLE]"
        output_uri (str, optional): URI where the output will be stored.
            Could be a BigQuery table or a Google Cloud Storage file.
            E.g. "gs://[BUCKET]/[OUTPUT].jsonl" OR "bq://[PROJECT].[DATASET].[TABLE]"
    Returns:
        batch_prediction_job: The batch prediction job object containing details of the job.
    """

    # [START generativeaionvertexai_batch_predict_gemini_createjob]

    # TODO(developer): Update and un-comment below lines
    # input_uri ="gs://[BUCKET]/[OUTPUT].jsonl"
    # output_uri ="gs://[BUCKET]"

    # Initialize vertexai
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    # Submit a batch prediction job with Gemini model
    batch_prediction_job = BatchPredictionJob.submit(
        source_model="gemini-1.5-flash-001",
        input_dataset=input_uri,
        output_uri_prefix=output_uri
    )

    # Check job status
    print(f"Job resouce name: {batch_prediction_job.resource_name}")
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
    #  Job output location: gs://yourbucket/gen-ai-batch-prediction/prediction-model-year-month-day-hour:minute:second.12345

    # [END generativeaionvertexai_batch_predict_gemini_createjob]

    return batch_prediction_job


if __name__ == "__main__":
    batch_gemini_prediction()
