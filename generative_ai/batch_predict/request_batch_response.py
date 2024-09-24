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


def request_batch_response(
    input_uri: str = None, output_uri: str = None
) -> BatchPredictionJob:
    """Perform batch text prediction using a pre-trained text generation model.
    Args:
        input_uri (str, optional): The input soure URI, which can be a BigQuery table or a file in a Cloud Storage bucket.
            E.g. "gs://[BUCKET]/[DATASET].jsonl" OR "bq://[PROJECT].[DATASET].[TABLE]"
        output_uri (str, optional): The URI where the output will be stored.
            This can be a BigQuery table or a file in a Cloud Storage bucket.
            E.g. "gs://[BUCKET]/[OUTPUT].jsonl" OR "bq://[PROJECT].[DATASET].[TABLE]"
    Returns:
        batch_prediction_job: The batch prediction job object containing details of the job.
    """

    # [START generativeaionvertexai_request_batch_response]
    import time

    from google.cloud.aiplatform_v1 import JobState
    import vertexai
    from vertexai.preview.batch_prediction import BatchPredictionJob

    JOB_POLL_INTERVAL = 15  # seconds

    # Example of using a BigQuery table as the input and output data source.
    # TODO (Developer): Replace the input_uri and output_uri with your own table names.
    # input_uri = "bq://[PROJECT_ID].vertexai_batch_predictions_inputs.text_prompts_culinary"
    # output_uri = "bq://[PROJECT_ID].vertexai_batch_predictions_outputs.results_culinary"

    # Initialize Vertex AI
    # TODO (developer): update project & location
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # Create batch prediction job.
    job = BatchPredictionJob.submit(
        source_model="gemini-1.5-flash-001",
        input_dataset=input_uri,
        output_uri_prefix=output_uri,
    )

    # Poll until the batch prediction job completes.
    while not job.has_ended:
        job.refresh()

        job_state = job.state

        if job_state in (JobState.JOB_STATE_QUEUED, JobState.JOB_STATE_PENDING):
            print("Waiting to start...")
        elif job_state == JobState.JOB_STATE_RUNNING:
            print("Working on it...")
        elif job_state == JobState.JOB_STATE_SUCCEEDED:
            print("Finished the job successfully")
        else:
            print(f"The job state is {job_state.name}")

        time.sleep(JOB_POLL_INTERVAL)

    print(f"Batch prediction job finished with state '{job_state.name}'")

    # [END generativeaionvertexai_request_batch_response]
    return job


if __name__ == "__main__":
    request_batch_response()
