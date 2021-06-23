#!/usr/bin/env python

# Copyright 2020 Google LLC
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

import os
import platform
import subprocess
import uuid

from google.cloud import storage
import pytest

SUFFIX = uuid.uuid4().hex[0:6]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
BUCKET_NAME = f"dataflow-gpu-test-{SUFFIX}"
IMAGE_NAME = f"dataflow/gpu-workers/test-{SUFFIX}:latest"
REGION = "us-central1"
ZONE = "us-central1-f"


@pytest.fixture(scope="session")
def bucket_name() -> str:
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(BUCKET_NAME)

    yield BUCKET_NAME

    bucket.delete(force=True)


@pytest.fixture(scope="session")
def configure_docker() -> None:
    subprocess.run(
        [
            "gcloud",
            "auth",
            "configure-docker",
        ]
    )


@pytest.fixture(scope="session")
def image_name(configure_docker: None) -> str:
    # See the `cloudbuild.yaml` for the configuration for this build.
    substitutions = {
        "_PYTHON_VERSION": platform.python_version(),
        "_IMAGE": IMAGE_NAME,
    }
    print(f"-- Cloud build substitutions: {substitutions}")
    subprocess.run(
        [
            "gcloud",
            "builds",
            "submit",
            f"--project={PROJECT}",
            f"--substitutions={','.join([k + '=' + v for k, v in substitutions.items()])}",
            "--timeout=30m",
            "--quiet",
        ],
        check=True,
    )

    yield f"gcr.io/{PROJECT}/{IMAGE_NAME}"

    # Delete the image when we're done.
    subprocess.run(
        [
            "gcloud",
            "container",
            "images",
            "delete",
            f"gcr.io/{PROJECT}/{IMAGE_NAME}",
            f"--project={PROJECT}",
            "--quiet",
        ],
        check=True,
    )


def test_end_to_end(bucket_name: str, image_name: str) -> None:
    # Run the Beam pipeline in Dataflow making sure GPUs are used.
    gpu_type = "nvidia-tesla-t4"
    subprocess.run(
        [
            "python",
            "landsat_view.py",
            f"--output-path-prefix=gs://{bucket_name}/outputs/",
            "--runner=DataflowRunner",
            f"--job_name=gpu-workers-{SUFFIX}",
            f"--project={PROJECT}",
            f"--region={REGION}",
            f"--temp_location=gs://{bucket_name}/temp",
            "--worker_machine_type=custom-1-13312-ext",
            "--disk_size_gb=300",
            f"--worker_harness_container_image={image_name}",
            f"--worker_zone={ZONE}",
            f"--experiments=worker_accelerator=type={gpu_type},count=1,install-nvidia-driver",
            "--experiments=use_runner_v2",
        ],
        check=True,
    )

    # Check that output files were created and are not empty.
    storage_client = storage.Client()
    output_files = list(storage_client.list_blobs(bucket_name, prefix="outputs/"))
    assert len(output_files) > 0, "No output files found"
    for output_file in output_files:
        assert output_file.size > 0, f"Output file is empty: {output_file.name}"
