# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
from typing import Optional

from google.cloud.aiplatform import BatchPredictionJob


def batch_gemini_prediction(
    input_uri: Optional[str] = None, output_uri: str = None
) -> BatchPredictionJob:
    """Perform batch text prediction using a Gemini AI model.
    Args:
        input_uri (str, optional): URI of the input dataset. Could be a BigQuery table or a Google Cloud Storage file.
            E.g. "bq://myproject.sampledataset.mypredictiontable OR gs://mybucket/sampledataset.json"
        output_uri (str, optional): URI where the output will be stored. Could be a BigQuery table or a Google Cloud Storage file.
            E.g. "bq://myproject.sampledataset.mypredictiontable OR gs://mybucket/sampledataset.jsonl"
    Returns:
        batch_prediction_job: The batch prediction job object containing details of the job.
    """

    # [START generativeaionvertexai_batch_predict_gemini_createjob]
    from google.cloud import aiplatform

    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    LOCATION = "us-central1"
    MODEL_ID = "gemini-1.5-flash-001"  # Replace with your model ID"
    # TODO (Developer): Update and un-comment below line
    # input_uri = bq://example_project.example_dataset.example_table or gs://mybucket/sampledataset.json
    # output_uri = bq://example_project.example_dataset.example_table or gs://mybucket/sampledataset.json

    # Initialize
    aiplatform.init(project=PROJECT_ID, location=LOCATION)

    # Create the batch prediction job using BatchPredictionJob
    batch_prediction_job = aiplatform.BatchPredictionJob.create(
        job_display_name="displayname",  # Replace with your desired name
        model_name=f"publishers/google/models/{MODEL_ID}",
        gcs_source=input_uri,
        gcs_destination_prefix=output_uri,
    )

    print(batch_prediction_job.display_name)
    print(batch_prediction_job.resource_name)
    print(batch_prediction_job.state)

    # Example response:
    # BatchPredictionJob run completed. Resource name: projects/12345678/locations/yourlocation/batchPredictionJobs/1234567

    # [END generativeaionvertexai_batch_predict_gemini_createjob]

    return batch_prediction_job


if __name__ == "__main__":
    batch_gemini_prediction()
