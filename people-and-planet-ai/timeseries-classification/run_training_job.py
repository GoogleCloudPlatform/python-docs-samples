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


def run(project: str, image: str, location: str = "us-central1", num_replicas: int = 4):
    client = aiplatform.gapic.JobServiceClient(
        client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    )
    response = client.create_custom_job(
        parent=f"projects/{project}/locations/{location}",
        custom_job={
            "display_name": "global-fishing-watch",
            "job_spec": {
                # https://cloud.google.com/vertex-ai/docs/training/distributed-training
                "worker_pool_specs": [
                    {
                        # Scheduler
                        "machine_spec": {"machine_type": "e2-standard-4"},
                        "replica_count": 1,
                        "container_spec": {
                            "image_uri": image,
                            "command": [],
                            "args": [],
                        },
                    },
                    {
                        # Workers
                        "machine_spec": {"machine_type": "e2-standard-4"},
                        "replica_count": num_replicas,
                        "container_spec": {
                            "image_uri": image,
                            "command": [],
                            "args": [],
                        },
                    },
                ]
            },
        },
    )
    print("response:", response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--image", required=True)
    parser.add_argument("--location", default="us-central1")
    parser.add_argument("--num-replicas", default=4, type=int)
    args = parser.parse_args()

    run(
        project=args.project,
        image=args.image,
        location=args.location,
        num_replicas=args.num_replicas,
    )
