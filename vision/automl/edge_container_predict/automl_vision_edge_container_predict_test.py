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
import tempfile
import time

import pytest

import automl_vision_edge_container_predict as predict  # noqa


IMAGE_FILE_PATH = os.path.join(os.path.dirname(__file__), 'test.jpg')
# The cpu docker gcs path is from 'Edge container tutorial'.
CPU_DOCKER_GCS_PATH = '{}'.format(
  'gcr.io/cloud-devrel-public-resources/gcloud-container-1.14.0:latest')
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
    subprocess.check_output(
        ['docker', 'pull', CPU_DOCKER_GCS_PATH],
        env={'DOCKER_API_VERSION': '1.38'})

    if os.environ.get('TRAMPOLINE_VERSION'):
        # Use /tmp
        model_path = tempfile.TemporaryDirectory()
    else:
        # Use project directory with Trampoline V1.
        model_path = tempfile.TemporaryDirectory(dir=os.path.dirname(__file__))
    print("Using model_path: {}".format(model_path))
    # Get the sample saved model.
    subprocess.check_output(
        ['gsutil', '-m', 'cp', SAMPLE_SAVED_MODEL, model_path.name])

    # Start the CPU docker.
    subprocess.Popen(['docker', 'run', '--rm', '--name', NAME, '-v',
                      model_path.name + ':/tmp/mounted_model/0001', '-p',
                      str(PORT_NUMBER) + ':8501', '-t',
                      CPU_DOCKER_GCS_PATH],
                     env={'DOCKER_API_VERSION': '1.38'})
    # Sleep a few seconds to wait for the container running.
    time.sleep(10)

    yield PORT_NUMBER

    # tear down
    # Stop the container.
    subprocess.check_output(
        ['docker', 'stop', NAME], env={'DOCKER_API_VERSION': '1.38'})
    # Remove the docker image.
    subprocess.check_output(
        ['docker', 'rmi', CPU_DOCKER_GCS_PATH],
        env={'DOCKER_API_VERSION': '1.38'})
    # Remove the temporery directory.
    model_path.cleanup()


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
