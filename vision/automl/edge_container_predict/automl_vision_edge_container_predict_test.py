#!/usr/bin/env python

# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for automl_vision_edge_container_predict.

The test will automatically start a container with a sample saved_model.pb,
send a request with one image, verify the response and delete the started
container.

If you want to try the test, please install
[gsutil tools](https://cloud.google.com/storage/docs/gsutil_install) and
[Docker CE](https://docs.docker.com/install/) first.

Examples:
sudo python -m pytest automl_vision_edge_container_predict_test.py
"""

import os
import subprocess
import time
import automl_vision_edge_container_predict as predict
import pytest


# The absolute path of the current file. This will locate the model_path when
# run docker containers.
ROOT_DIR = os.environ.get(
    'KOKORO_ROOT', os.path.abspath(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(ROOT_DIR, 'model_path')

IMAGE_FILE_PATH = os.path.join(os.path.dirname(__file__), 'test.jpg')
# The cpu docker gcs path is from 'Edge container tutorial'.
CPU_DOCKER_GCS_PATH = '{}'.format(
  'gcr.io/automl-vision-ondevice/gcloud-container-1.12.0:latest')
# The path of a sample saved model.
SAMPLE_SAVED_MODEL = '{}'.format(
    'gs://cloud-samples-data/vision/edge_container_predict/saved_model.pb')
# Container Name.
NAME = 'AutomlVisionEdgeContainerPredictTest'
# Port Number.
PORT_NUMBER = 8505


@pytest.fixture
def edge_container_predict_server_port():
    # set up
    # Pull the CPU docker.
    subprocess.check_output(['docker', 'pull', CPU_DOCKER_GCS_PATH])

    # Get the sample saved model.
    if not os.path.exists(MODEL_PATH):
        os.mkdir(MODEL_PATH)
    subprocess.check_output(
            ['gsutil', '-m', 'cp', SAMPLE_SAVED_MODEL, MODEL_PATH])

    # Start the CPU docker.
    subprocess.Popen(['docker', 'run', '--rm', '--name', NAME, '-v',
                      MODEL_PATH + ':/tmp/mounted_model/0001', '-p',
                      str(PORT_NUMBER) + ':8501', '-t',
                      CPU_DOCKER_GCS_PATH])
    # Sleep a few seconds to wait for the container running.
    time.sleep(10)

    yield PORT_NUMBER

    # tear down
    # Stop the container.
    subprocess.check_output(['docker', 'stop', NAME])
    # Remove the docker image.
    subprocess.check_output(['docker', 'rmi', CPU_DOCKER_GCS_PATH])


def test_edge_container_predict(capsys, edge_container_predict_server_port):
    # If you send requests with one image each time, the key value does not
    # matter. If you send requests with multiple images, please used different
    # keys to indicated different images, which can make sure that the
    # responses corresponding to the given image.
    image_key = '1'
    # Send a request.
    response = predict.container_predict(
            IMAGE_FILE_PATH, image_key, PORT_NUMBER)
    # Verify the response.
    assert 'predictions' in response
    assert 'key' in response['predictions'][0]
    assert image_key == response['predictions'][0]['key']
