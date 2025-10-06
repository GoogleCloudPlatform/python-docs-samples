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

from google.genai import types


def get_batch_job(batch_job_name: str) -> types.BatchJob:
    # [START googlegenaisdk_batch_job_get]
    from google import genai
    from google.genai.types import HttpOptions

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    # Get the batch job
    # Eg. batch_job_name = "projects/123456789012/locations/ABCDEF/batchPredictionJobs/1234567890123456789"
    batch_job = client.batches.get(name=batch_job_name)

    print(f"Job state: {batch_job.state}")
    # Example response:
    # Job state: JOB_STATE_PENDING
    # Job state: JOB_STATE_RUNNING
    # Job state: JOB_STATE_SUCCEEDED

    # [END googlegenaisdk_batch_job_get]
    return batch_job


if __name__ == "__main__":
    try:
        get_batch_job(input("Batch job name: "))
    except Exception as e:
        print(f"An error occurred: {e}")
