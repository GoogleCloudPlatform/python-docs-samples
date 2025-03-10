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

from vertexai.tuning import sft

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def gemini_tuning_basic() -> sft.SupervisedTuningJob:
    # [START generativeaionvertexai_tuning_basic]

    import time

    import vertexai
    from vertexai.tuning import sft

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    sft_tuning_job = sft.train(
        source_model="gemini-2.0-flash-001",
        # 1.5 and 2.0 models use the same JSONL format
        train_dataset="gs://cloud-samples-data/ai-platform/generative_ai/gemini-1_5/text/sft_train_data.jsonl",
    )

    # Polling for job completion
    while not sft_tuning_job.has_ended:
        time.sleep(60)
        sft_tuning_job.refresh()

    print(sft_tuning_job.tuned_model_name)
    print(sft_tuning_job.tuned_model_endpoint_name)
    print(sft_tuning_job.experiment)
    # Example response:
    # projects/123456789012/locations/us-central1/models/1234567890@1
    # projects/123456789012/locations/us-central1/endpoints/123456789012345
    # <google.cloud.aiplatform.metadata.experiment_resources.Experiment object at 0x7b5b4ae07af0>

    # [END generativeaionvertexai_tuning_basic]
    return sft_tuning_job


if __name__ == "__main__":
    gemini_tuning_basic()
