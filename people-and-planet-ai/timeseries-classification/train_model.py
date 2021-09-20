# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from google.cloud import aiplatform


def run(
    project: str,
    region: str,
    container_image: str,
    train_data_dir: str,
    eval_data_dir: str,
    training_dir: str,
    train_epochs: int,
    batch_size: int,
    machine_type: str,
    gpu_type: str,
    gpu_count: str,
) -> str:
    client = aiplatform.gapic.JobServiceClient(
        client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    )
    response = client.create_custom_job(
        parent=f"projects/{project}/locations/{region}",
        custom_job={
            "display_name": "global-fishing-watch",
            "job_spec": {
                # https://cloud.google.com/vertex-ai/docs/reference/rest/v1/CustomJobSpec
                "base_output_directory": {
                    "output_uri_prefix": training_dir,
                },
                # https://cloud.google.com/vertex-ai/docs/training/distributed-training
                "worker_pool_specs": [
                    {
                        "replica_count": 1,
                        "machine_spec": {
                            "machine_type": machine_type,
                            "accelerator_type": gpu_type,
                            "accelerator_count": gpu_count,
                        },
                        "container_spec": {
                            "image_uri": container_image,
                            "command": ["python"],
                            "args": [
                                "trainer.py",
                                f"--train-data-dir={train_data_dir}",
                                f"--eval-data-dir={eval_data_dir}",
                                f"--train-epochs={train_epochs}",
                                f"--batch-size={batch_size}",
                            ],
                        },
                    },
                ],
            },
        },
    )
    logging.info("Vertex AI job response:")
    logging.info(response)
    return response.name.split("/")[-1]
