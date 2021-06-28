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

import argparse

from google.cloud import aiplatform


def run(
    project: str,
    bucket: str,
    location: str,
    storage_dir: str,
    image: str,
    train_steps: int,
    eval_steps: int,
    num_workers: int = 4,
):
    client = aiplatform.gapic.JobServiceClient(
        client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    )
    response = client.create_custom_job(
        parent=f"projects/{project}/locations/{location}",
        custom_job={
            "display_name": "global-fishing-watch",
            "job_spec": {
                # https://cloud.google.com/vertex-ai/docs/reference/rest/v1/CustomJobSpec
                "base_output_directory": {
                    "output_uri_prefix": f"gs://{bucket}/{storage_dir}",
                },
                # https://cloud.google.com/vertex-ai/docs/training/distributed-training
                "worker_pool_specs": [
                    {
                        # Scheduler
                        "machine_spec": {"machine_type": "e2-standard-4"},
                        "replica_count": 1,
                        "container_spec": {
                            "image_uri": f"gcr.io/{project}/{image}",
                            "command": ["python"],
                            "args": [
                                "trainer.py",
                                f"--train-data-dir=gs://{bucket}/{storage_dir}/datasets/train",
                                f"--eval-data-dir=gs://{bucket}/{storage_dir}/datasets/eval",
                                f"--train-steps={train_steps}",
                                f"--eval-steps={eval_steps}",
                            ],
                        },
                    },
                    # TODO: figure out how to use multiple workers for training
                    # {
                    #     # Workers
                    #     "machine_spec": {"machine_type": "e2-standard-4"},
                    #     "replica_count": num_workers,
                    #     "container_spec": {
                    #         "image_uri": f"gcr.io/{project}/{image}",
                    #         "command": ["python"],
                    #         "args": [
                    #             "trainer.py",
                    #             f"--train-data-dir=gs://{bucket}/{storage_dir}/datasets/train",
                    #             f"--eval-data-dir=gs://{bucket}/{storage_dir}/datasets/eval",
                    #             f"--train-steps={train_steps}",
                    #             f"--eval-steps={eval_steps}",
                    #         ],
                    #     },
                    # },
                ],
            },
        },
    )
    print("response:", response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--location", required=True)
    parser.add_argument("--storage-dir", default="samples/global-fishing-watch")
    parser.add_argument("--image", default="samples/global-fishing-watch:latest")
    parser.add_argument("--train-steps", default=1000, type=int)
    parser.add_argument("--eval-steps", default=100, type=int)
    parser.add_argument("--num-workers", default=4, type=int)
    args = parser.parse_args()

    run(
        project=args.project,
        bucket=args.bucket,
        location=args.location,
        storage_dir=args.storage_dir,
        image=args.image,
        train_steps=args.train_steps,
        eval_steps=args.eval_steps,
        num_workers=args.num_workers,
    )
