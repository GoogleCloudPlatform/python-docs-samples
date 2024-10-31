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
    import time
    import vertexai

    from vertexai.batch_prediction import BatchPredictionJob

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"

    # Initialize vertexai
    vertexai.init(project=PROJECT_ID, location="us-central1")

    input_uri = "bq://storage-samples.generative_ai.batch_requests_for_multimodal_input"

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
    #  Job output location: bq://Project-ID/gen-ai-batch-prediction/predictions-model-year-month-day-hour:minute:second.12345
    # [END generativeaionvertexai_batch_predict_gemini_createjob_bigquery]
    return batch_prediction_job


if __name__ == "__main__":
    batch_predict_gemini_createjob(output_uri)
