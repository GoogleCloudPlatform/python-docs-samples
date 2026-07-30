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

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


def prompts_custom_job_example(
    cloud_bucket: str, config_path: str, output_path: str
) -> str:
    """Improve prompts by evaluating the model's response to sample prompts against specified evaluation metric(s).
    Args:
        cloud_bucket(str): Specify the Google Cloud Storage bucket to store outputs and metadata. For example, gs://bucket-name
        config_path(str): Filepath for config file in your Google Cloud Storage bucket. For example, prompts/custom_job/instructions/configuration.json
        output_path(str): Filepath of the folder location in your Google Cloud Storage bucket. For example, prompts/custom_job/output
    Returns(str):
        Resource name of the job created. For example, projects/<project-id>/locations/location/customJobs/<job-id>
    """
    #  [START generativeaionvertexai_prompt_optimizer]
    from google.cloud import aiplatform

    # Initialize Vertex AI platform
    aiplatform.init(project=PROJECT_ID, location="us-central1")

    # TODO(Developer): Check and update lines below
    # cloud_bucket = "gs://cloud-samples-data"
    # config_path = f"{cloud_bucket}/instructions/sample_configuration.json"
    # output_path = "custom_job/output/"

    custom_job = aiplatform.CustomJob(
        display_name="Prompt Optimizer example",
        worker_pool_specs=[
            {
                "replica_count": 1,
                "container_spec": {
                    "image_uri": "us-docker.pkg.dev/vertex-ai-restricted/builtin-algorithm/apd:preview_v1_0",
                    "args": [f"--config={cloud_bucket}/{config_path}"],
                },
                "machine_spec": {
                    "machine_type": "n1-standard-4",
                },
            }
        ],
        staging_bucket=cloud_bucket,
        base_output_dir=f"{cloud_bucket}/{output_path}",
    )

    custom_job.submit()
    print(f"Job resource name: {custom_job.resource_name}")
    # Example response:
    #    'projects/123412341234/locations/us-central1/customJobs/12341234123412341234'
    #  [END generativeaionvertexai_prompt_optimizer]
    return custom_job.resource_name


if __name__ == "__main__":
    prompts_custom_job_example(
        os.environ["CLOUD_BUCKET"],
        os.environ["JSON_CONFIG_PATH"],
        os.environ["OUTPUT_PATH"],
    )
