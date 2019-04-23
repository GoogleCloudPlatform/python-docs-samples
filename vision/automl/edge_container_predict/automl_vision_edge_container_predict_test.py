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

The test will automatically start a container with a sample saved_model.pb, send
a request with one image, verify the response and delete the started container.

If you want to try the test, please install
[gsutil tools](https://cloud.google.com/storage/docs/gsutil_install) and
[Docker CE](https://docs.docker.com/install/) first.

Examples:
sudo python automl_vision_edge_container_predict_test.py
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import subprocess
import time
import unittest
import automl_vision_edge_container_predict as predict

# The absolute path of the current file. This will locate the model_path when
# run docker containers.
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
# The cpu docker gcs path is from 'Edge container tutorial'.
CPU_DOCKER_GCS_PATH = 'gcr.io/automl-vision-ondevice/gcloud-container-1.12.0:latest'
# The path of a sample saved model.
SAMPLE_SAVED_MODEL = 'gs://cloud-samples-data/vision/edge_container_predict/saved_model.pb'


class AutomlVisionEdgeContainerPredictTest(unittest.TestCase):

  def setUp(self):
    super(AutomlVisionEdgeContainerPredictTest, self).setUp()
    print('Pull the CPU docker.')
    subprocess.check_output(['docker', 'pull', CPU_DOCKER_GCS_PATH])
    print('Get the sample saved model.')
    self.model_path = os.path.join(ROOT_DIR, 'model_path')
    if not os.path.exists(self.model_path):
      os.mkdir(self.model_path)
    subprocess.check_output(['gsutil', '-m', 'cp', SAMPLE_SAVED_MODEL,
                             self.model_path])

  def test_prediction(self):
    print('Start the CPU docker.')
    self.name = 'AutomlVisionEdgeContainerPredictTest'
    self.port_number = 8501
    subprocess.Popen(['docker', 'run', '--rm', '--name', self.name, '-v',
                      self.model_path + ':/tmp/mounted_model/0001', '-p',
                      str(self.port_number) + ':8501', '-t',
                      CPU_DOCKER_GCS_PATH])
    # Sleep a few seconds to wait for the container running.
    time.sleep(10)

    image_file_path = 'test.jpg'
    # If you send requests with one image each time, the key value does not
    # matter. If you send requests with multiple images, please used different
    # keys to indicated different images.
    image_key = '1'
    print('Send a request.')
    response = predict.container_predict(
        image_file_path, image_key, self.port_number)
    print('The response is: ')
    print(response)

    print('Stop the container: ' + self.name)
    subprocess.check_output(['docker', 'stop', self.name])

    self.assertIn('predictions', response)
    self.assertIn('key', response['predictions'][0])
    self.assertEqual(image_key, response['predictions'][0]['key'])

  def tearDown(self):
    print('Remove the docker image ' + CPU_DOCKER_GCS_PATH)
    subprocess.check_output(['docker', 'rmi', CPU_DOCKER_GCS_PATH])
    super(AutomlVisionEdgeContainerPredictTest, self).tearDown()

if __name__ == '__main__':
  unittest.main()
