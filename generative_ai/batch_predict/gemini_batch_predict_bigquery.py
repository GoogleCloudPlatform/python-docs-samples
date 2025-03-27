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

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

output_uri = "bq://storage-samples.generative_ai.gen_ai_batch_prediction.predictions"


def batch_predict_gemini_createjob(output_uri: str) -> str:
    """Perform batch text prediction using a Gemini AI model and returns the output location"""

    # [START generativeaionvertexai_batch_predict_gemini_createjob_bigquery]
    import google.cloud.aiplatform as aiplatform

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"

    # Initialize aiplatform
    aiplatform.init(project=PROJECT_ID, location="us-central1")

    input_uri = "bq://storage-samples.generative_ai.batch_requests_for_multimodal_input"

    # Submit a batch prediction job with Gemini model
    batch_prediction_job = aiplatform.BatchPredictionJob.create(
        model_name=f"projects/{PROJECT_ID}/locations/us-central1/publishers/google/models/gemini-1.5-flash-002",
        job_display_name="Batch predict with Gemini - BigQuery",
        bigquery_source=input_uri,
        bigquery_destination_prefix=output_uri,
    )

    # Check job status
    print(f"Job resource name: {batch_prediction_job.resource_name}")

    # Example response:
    # BatchPredictionJob created. Resource name: projects/12345678/locations/us-central1/batchPredictionJobs/12345678
    # BatchPredictionJob run completed. Resource name: projects/12345678/locations/us-central1/batchPredictionJobs/12345678

    # [END generativeaionvertexai_batch_predict_gemini_createjob_bigquery]
    return batch_prediction_job


if __name__ == "__main__":
    batch_predict_gemini_createjob(output_uri)
