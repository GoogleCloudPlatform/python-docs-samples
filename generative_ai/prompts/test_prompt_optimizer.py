# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import time

from google.cloud import aiplatform, storage
from google.cloud.aiplatform_v1 import JobState

from prompt_optimizer import prompts_custom_job_example

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
CLOUD_BUCKET = "gs://python-docs-samples-tests"
CONFIG_PATH = "ai-platform/prompt_optimization/instructions/sample_configuration.json"
OUTPUT_PATH = "ai-platform/prompt_optimization/output/"


def test_prompt_optimizer() -> None:
    custom_job_name = prompts_custom_job_example(CLOUD_BUCKET, CONFIG_PATH, OUTPUT_PATH)
    job = aiplatform.CustomJob.get(
        resource_name=custom_job_name, project=PROJECT_ID, location="us-central1"
    )

    storage_client = storage.Client()
    start_time = time.time()
    timeout = 1200

    try:
        while (
            job.state not in [JobState.JOB_STATE_SUCCEEDED, JobState.JOB_STATE_FAILED]
            and time.time() - start_time < timeout
        ):
            print(f"Waiting for the CustomJob({job.resource_name}) to be ready!")
            time.sleep(10)
        assert (
            storage_client.get_bucket(CLOUD_BUCKET.split("gs://")[-1]).list_blobs(
                prefix=OUTPUT_PATH
            )
            is not None
        )
    finally:
        # delete job
        print(f"CustomJob({job.resource_name}) to be ready. Delete it now.")
        job.delete()
        # delete output blob
        blobs = storage_client.get_bucket(CLOUD_BUCKET.split("gs://")[-1]).list_blobs(
            prefix=OUTPUT_PATH
        )
        for blob in blobs:
            blob.delete()
