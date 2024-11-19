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

output_uri = "gs://python-docs-samples-tests"


def batch_predict_gemini_createjob(output_uri: str) -> str:
    "Perform batch text prediction using a Gemini AI model and returns the output location"

    # [START generativeaionvertexai_batch_predict_gemini_createjob]
    import google.cloud.aiplatform as aiplatform

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"

    # Initialize aiplatform
    aiplatform.init(project=PROJECT_ID, location="us-central1")

    input_uri = "gs://cloud-samples-data/batch/prompt_for_batch_gemini_predict.jsonl"

    # Submit a batch prediction job with Gemini model
    batch_prediction_job = aiplatform.BatchPredictionJob.create(
        model_name=f"projects/{PROJECT_ID}/locations/us-central1/publishers/google/models/gemini-1.5-flash-002",
        job_display_name="Batch predict with Gemini - GCS",
        gcs_source=input_uri,
        gcs_destination_prefix=output_uri,
    )

    # Check job status
    print(f"Job resource name: {batch_prediction_job.resource_name}")

    # Example response:
    # View Batch Prediction Job: https://console.cloud.google.com/ai/platform/locations/us-central1/batch-predictions/12345678?project=projectid
    # BatchPredictionJob created. Resource name: projects/1234567/locations/us-central1/batchPredictionJobs/1234567
    # BatchPredictionJob run completed. Resource name: projects/650231661283/locations/us-central1/batchPredictionJobs/2544655663456321536

    # [END generativeaionvertexai_batch_predict_gemini_createjob]
    return batch_prediction_job


if __name__ == "__main__":
    batch_predict_gemini_createjob(output_uri)
