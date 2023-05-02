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

from google.cloud import aiplatform


def run(
    project: str,
    region: str,
    train_data_dir: str,
    eval_data_dir: str,
    training_dir: str,
    train_epochs: int,
    batch_size: int,
    machine_type: str,
    gpu_type: str,
    gpu_count: str,
    sync: bool,
) -> None:
    bucket = training_dir.removeprefix('gs://').split('/')[0]

    aiplatform.init(project=project, location=region, staging_bucket=bucket)

    # Launch the custom training job.
    job = aiplatform.CustomTrainingJob(
        display_name="global-fishing-watch",
        script_path="trainer.py",
        container_uri="us-docker.pkg.dev/vertex-ai/training/tf-gpu.2-11:latest",
    )
    job.run(
        machine_type=machine_type,
        accelerator_type=gpu_type,
        accelerator_count=gpu_count,
        args=[
            f"--train-data-dir={train_data_dir}",
            f"--eval-data-dir={eval_data_dir}",
            f"--train-epochs={train_epochs}",
            f"--batch-size={batch_size}",
        ],
        sync=sync,
    )
