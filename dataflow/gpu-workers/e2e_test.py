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
import subprocess
import uuid

from google.cloud import storage
import pytest

SUFFIX = uuid.uuid4().hex[0:6]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
BUCKET_NAME = f"dataflow-gpu-test-{SUFFIX}"
IMAGE_NAME = f"gcr.io/{PROJECT}/dataflow/gpu-workers/test-{SUFFIX}"

# TODO: REMOVE THIS AND DELETE RESOURCES
BUCKET_NAME = f"dataflow-gpu-test"
IMAGE_NAME = f"gcr.io/{PROJECT}/dataflow/gpu-workers/test"


@pytest.fixture
def bucket_name() -> str:
    client = storage.Client()
    bucket = client.create_bucket(BUCKET_NAME)

    yield BUCKET_NAME

    # bucket.delete()


@pytest.fixture
def image_name() -> str:
    subprocess.run(
        [
            "gcloud",
            "builds",
            "submit",
            f"--project={PROJECT}",
            f"--tag={IMAGE_NAME}",
            "--timeout=30m",
            "--quiet",
        ],
        check=True,
    )

    yield IMAGE_NAME

    # subprocess.run(
    #     [
    #         "gcloud",
    #         "container",
    #         "images",
    #         "delete",
    #         IMAGE_NAME,
    #         f"--project={PROJECT}",
    #         "--quiet",
    #     ],
    #     check=True,
    # )


def test_python_version(image_name: str) -> None:
    # Make sure the local and Docker Python versions are the same.
    # If this test fails, the following needs updating:
    # - noxfile_config.py: The Python 'ignored_versions' should only allow the Dockerfile Python version.
    # - Dockerfile: The `COPY --from=apache/beam` for the worker boot file.
    # - Docs tutorial: https://cloud.google.com/dataflow/docs/samples/satellite-images-gpus
    subprocess.run([
        # docker run --rm -it --entrypoint=/bin/bash $IMAGE -c "python --version"
        'docker',
        'run',
        '--rm',
        '-it',
        '--entrypoint=/bin/bash',
        image_name,
        '-c'
        'python --version'
    ])


def test_apache_beam_version() -> None:
    # Make sure the installed Apache Beam version matches the Apache Beam image
    # we use to copy the worker boot file.
    # If this test fails, the following needs updating:
    # - Dockerfile: The `COPY --from=apache/beam` for the worker boot file.
    pass


def test_tensorflow_version() -> None:
    # Make sure the installed Tensorflow version matches the Tensorflow version
    # in the Dockerfile.
    # If this test fails, the following needs updating:
    # - Dockerfile: The `FROM tensorflow/tensorflow` version.
    pass


def test_end_to_end(bucket_name: str, image_name: str) -> None:
    # Run the Beam pipeline in Dataflow making sure GPUs are used.
    gpu_type = "nvidia-tesla-t4"
    subprocess.run(
        [
            "python",
            "landsat_view.py",
            "--scene=LC08_L1TP_115078_20200608_20200625_01_T1",
            f"--output-path-prefix=gs://{bucket_name}/outputs/",
            "--gpu-required",
            "--runner=DataflowRunner",
            f"--project={PROJECT}",
            "--region=us-east1",
            "--worker_machine_type=custom-1-13312-ext",
            f"--worker_harness_container_image={image_name}",
            "--worker_zone=us-east1-a",
            f"--experiments=worker_accelerator=type={gpu_type},count=1,install-nvidia-driver",
            "--experiments=use_runner_v2",
        ],
        check=True,
    )

    # Check that the output file was created and is not empty.
    client = storage.Client()
    output = client.get_bucket(bucket_name).get_blob(
        "outputs/LC08_L1TP_115078_20200608_20200625_01_T1.jpeg"
    )
    assert output.size > 0
