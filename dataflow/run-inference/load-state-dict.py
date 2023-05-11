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

"""Loads the state_dict for an LLM model into Cloud Storage."""

from __future__ import annotations

import os

import torch
from transformers import AutoModelForSeq2SeqLM


def run_local(model_name: str, state_dict_path: str) -> None:
    """Loads the state dict and saves it into the desired path.

    If the `state_dict_path` is a Cloud Storage location starting
    with "gs://", this assumes Cloud Storage is mounted with
    Cloud Storage FUSE in `/gcs`. Vertex AI is set up like this.

    Args:
        model_name: HuggingFace model name compatible with AutoModelForSeq2SeqLM.
        state_dict_path: File path to the model's state_dict, can be in Cloud Storage.
    """
    print(f"Loading model: {model_name}")
    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name, torch_dtype=torch.bfloat16
    )
    print(f"Model loaded, saving state dict to: {state_dict_path}")

    # Assume Cloud Storage FUSE is mounted in `/gcs`.
    state_dict_path = state_dict_path.replace("gs://", "/gcs/")
    os.makedirs(os.path.dirname(state_dict_path), exist_ok=True)
    torch.save(model.state_dict(), state_dict_path)
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
    """Launches a Vertex AI custom job to load the state dict.

    If the model is too large to fit into memory or disk, we can launch
    a Vertex AI custom job with a large enough VM for this to work.

    Depending on the model's size, it might require a different VM
    configuration. The model MUST fit into the VM's memory, and there
    must be enough disk space to stage the entire model while it gets
    copied to Cloud Storage.

    Args:
        model_name: HuggingFace model name compatible with AutoModelForSeq2SeqLM.
        state_dict_path: File path to the model's state_dict, can be in Cloud Storage.
        job_name: Job display name in the Vertex AI console.
        project: Google Cloud Project ID.
        bucket: Cloud Storage bucket name, without the "gs://" prefix.
        location: Google Cloud regional location.
        machine_type: Machine type for the VM to run the job.
        disk_size_gb: Disk size in GB for the VM to run the job.
    """
    from google.cloud import aiplatform

    aiplatform.init(project=project, staging_bucket=bucket, location=location)

    job = aiplatform.CustomJob.from_local_script(
        display_name=job_name,
        container_uri="us-docker.pkg.dev/vertex-ai/training/pytorch-gpu.1-13:latest",
        script_path="load-state-dict.py",
        args=[
            "local",
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
    subparsers = parser.add_subparsers(required=True)

    parser_local = subparsers.add_parser("local")
    parser_local.add_argument(
        "--model-name",
        required=True,
        help="HuggingFace model name compatible with AutoModelForSeq2SeqLM",
    )
    parser_local.add_argument(
        "--state-dict-path",
        required=True,
        help="File path to the model's state_dict, can be in Cloud Storage",
    )
    parser_local.set_defaults(run=run_local)

    parser_vertex = subparsers.add_parser("vertex")
    parser_vertex.add_argument(
        "--model-name",
        required=True,
        help="HuggingFace model name compatible with AutoModelForSeq2SeqLM",
    )
    parser_vertex.add_argument(
        "--state-dict-path",
        required=True,
        help="File path to the model's state_dict, can be in Cloud Storage",
    )
    parser_vertex.add_argument(
        "--job-name", required=True, help="Job display name in the Vertex AI console"
    )
    parser_vertex.add_argument(
        "--project", required=True, help="Google Cloud Project ID"
    )
    parser_vertex.add_argument(
        "--bucket",
        required=True,
        help='Cloud Storage bucket name, without the "gs://" prefix',
    )
    parser_vertex.add_argument(
        "--location", default="us-central1", help="Google Cloud regional location"
    )
    parser_vertex.add_argument(
        "--machine-type",
        default="e2-highmem-2",
        help="Machine type for the VM to run the job",
    )
    parser_vertex.add_argument(
        "--disk-size-gb",
        type=int,
        default=100,
        help="Disk size in GB for the VM to run the job",
    )
    parser_vertex.set_defaults(run=run_vertex_job)

    args = parser.parse_args()
    kwargs = args.__dict__.copy()
    kwargs.pop("run")

    args.run(**kwargs)
