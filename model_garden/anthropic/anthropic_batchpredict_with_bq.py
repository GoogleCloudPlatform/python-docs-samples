# Copyright 2025 Google LLC
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


def generate_content(output_uri: str) -> str:
    # [START aiplatform_anthropic_batchpredict_with_bq]
    import time

    from google import genai
    from google.genai.types import CreateBatchJobConfig, JobState, HttpOptions

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    # TODO(developer): Update and un-comment below line
    # output_uri = f"bq://your-project.your_dataset.your_table"

    job = client.batches.create(
        # Check Anthropic Claude region availability in https://cloud.devsite.corp.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude#regions
        # More about Anthropic model: https://console.cloud.google.com/vertex-ai/publishers/anthropic/model-garden/claude-3-5-haiku
        model="publishers/anthropic/models/claude-3-5-haiku",
        # The source dataset needs to be created specifically in us-east5
        src="bq://python-docs-samples-tests.anthropic_bq_sample.test_data",
        config=CreateBatchJobConfig(dest=output_uri),
    )
    print(f"Job name: {job.name}")
    print(f"Job state: {job.state}")
    # Example response:
    # Job name: projects/%PROJECT_ID%/locations/us-central1/batchPredictionJobs/9876453210000000000
    # Job state: JOB_STATE_PENDING

    # See the documentation: https://googleapis.github.io/python-genai/genai.html#genai.types.BatchJob
    completed_states = {
        JobState.JOB_STATE_SUCCEEDED,
        JobState.JOB_STATE_FAILED,
        JobState.JOB_STATE_CANCELLED,
        JobState.JOB_STATE_PAUSED,
    }

    while job.state not in completed_states:
        time.sleep(30)
        job = client.batches.get(name=job.name)
        print(f"Job state: {job.state}")
    # Example response:
    # Job state: JOB_STATE_PENDING
    # Job state: JOB_STATE_RUNNING
    # Job state: JOB_STATE_RUNNING
    # ...
    # Job state: JOB_STATE_SUCCEEDED

    # [END aiplatform_anthropic_batchpredict_with_bq]
    return job.state


if __name__ == "__main__":
    # The dataset of the output uri needs to be created specifically in us-east5
    generate_content(output_uri="bq://your-project.your_dataset.your_table")
