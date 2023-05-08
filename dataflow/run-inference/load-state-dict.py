# Copyright 2023 Google LLC
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

from __future__ import annotations

from transformers import AutoModelForSeq2SeqLM
import torch


def run_local(model_name: str, state_dict_path: str) -> None:
    print(f"Loading model: {model_name}")
    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name, torch_dtype=torch.bfloat16
    )
    print(f"Model loaded, saving state dict to: {state_dict_path}")
    torch.save(model.state_dict(), state_dict_path.replace("gs://", "/gcs/"))
    print("State dict saved successfully!")


def run_vertex_job(
    model_name: str,
    state_dict_path: str,
    job_name: str,
    project: str,
    bucket: str,
    location: str = "us-central1",
    machine_type: str = "e2-highmem-2",
    disk_size_gb: int = 100,
) -> None:
    from google.cloud import aiplatform

    aiplatform.init(project=project, staging_bucket=bucket, location=location)

    job = aiplatform.CustomJob.from_local_script(
        display_name=job_name,
        container_uri="us-docker.pkg.dev/vertex-ai/training/pytorch-gpu.1-13:latest",
        script_path="load-state-dict.py",
        args=[
            f"--model-name={model_name}",
            f"--state-dict-path={state_dict_path}",
        ],
        machine_type=machine_type,
        boot_disk_size_gb=disk_size_gb,
        requirements=["transformers"],
    )
    job.run()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model-name", required=True)
    parser.add_argument("--state-dict-path", required=True)
    parser.add_argument("--job-name", type=str)
    args, vertex_job_args = parser.parse_known_args()

    model_name = args.model_name
    state_dict_path = args.state_dict_path
    job_name = args.job_name

    if job_name:
        parser = argparse.ArgumentParser()
        parser.add_argument("--project", required=True)
        parser.add_argument("--bucket", required=True)
        parser.add_argument("--location", default="us-central1")
        parser.add_argument("--machine-type", default="e2-highmem-2")
        parser.add_argument("--disk-size-gb", type=int, default=100)
        args, job_args = parser.parse_known_args()

        run_vertex_job(
            model_name=model_name,
            state_dict_path=state_dict_path,
            job_name=job_name,
            project=args.project,
            bucket=args.bucket,
            location=args.location,
            machine_type=args.machine_type,
            disk_size_gb=args.disk_size_gb,
        )

    else:
        run_local(model_name, state_dict_path)
