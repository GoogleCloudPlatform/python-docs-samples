# Copyright 2017 Google Inc. All Rights Reserved.
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

import os
import time
import uuid

import cloudiot_pubsub_example_server as example_server

cloud_region = 'us-central1'
device_id_template = 'test-device-{}'
topic_id = f'test-device-events-topic-{int(time.time())}'

project_id = os.environ['GOOGLE_CLOUD_PROJECT']
service_account_json = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

pubsub_topic = f'projects/{project_id}/topics/{topic_id}'
registry_id = f'test-registry-{uuid.uuid4().hex}-{int(time.time())}'


def test_config_turn_on(capsys):
    max_temp = 11
    data = {'temperature': max_temp}

    Server = example_server.Server(service_account_json)
    Server._update_device_config(
        project_id,
        cloud_region,
        registry_id,
        device_id_template,
        data)

    stdout, _ = capsys.readouterr()
    assert 'on' in stdout
    assert '11' in stdout
    assert 'test-device-{}' in stdout


def test_config_turn_off(capsys):
    min_temp = -1
    data = {'temperature': min_temp}

    Server = example_server.Server(service_account_json)
    Server._update_device_config(
        project_id,
        cloud_region,
        registry_id,
        device_id_template,
        data)

    stdout, _ = capsys.readouterr()
    assert 'off' in stdout
    assert '-1' in stdout
    assert 'test-device-{}' in stdout
