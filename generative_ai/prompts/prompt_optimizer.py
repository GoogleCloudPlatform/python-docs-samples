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

from google.cloud import aiplatform


#  [START aiplatform_prompt_optimizer]
def optimize_prompts(
    project: str,
    location: str,
    staging_bucket: str,
    configuration_path: str,
) -> None:

    aiplatform.init(project=project, location=location, staging_bucket=staging_bucket)

    worker_pool_specs = [{
        "replica_count": 1,
        "container_spec": {
            "image_uri": "us-docker.pkg.dev/vertex-ai-restricted/builtin-algorithm/apd:preview_v1_0",
            "args": [f"--config={configuration_path}"]
        },
        "machine_spec": {
            "machine_type": "n1-standard-4",
        },
    }]

    custom_job = aiplatform.CustomJob(
        display_name="Prompt Optimizer example",
        worker_pool_specs=worker_pool_specs,
    )
    custom_job.submit()

#  [END aiplatform_prompt_optimizer]


if __name__ == "__main__":
    optimize_prompts(os.environ["PROJECT_ID"], "us-central1", os.environ["PROMPT_OPTIMIZER_BUCKET_NAME"], os.environ["CONFIG_PATH"])
