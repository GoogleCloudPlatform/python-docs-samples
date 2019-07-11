# Copyright 2019 Google Inc. All Rights Reserved.
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
import argparse
import os
import sys
import time

from google.cloud import pubsub

# Add manager as library
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'manager'))  # noqa
import manager

import mock
import pytest

import cloudiot_mqtt_example
import cloudiot_mqtt_image


cloud_region = 'us-central1'
device_id_template = 'test-device-{}'
ca_cert_path = 'resources/roots.pem'
rsa_cert_path = 'resources/rsa_cert.pem'
rsa_private_path = 'resources/rsa_private.pem'
topic_id = 'test-device-events-{}'.format(int(time.time()))

project_id = os.environ['GCLOUD_PROJECT']
service_account_json = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

pubsub_topic = 'projects/{}/topics/{}'.format(project_id, topic_id)
registry_id = 'test-registry-{}'.format(int(time.time()))

image_path='./resources/owlister_hootie.png'

mqtt_bridge_hostname = 'mqtt.googleapis.com'
mqtt_bridge_port = 443


@pytest.fixture(scope='module')
def test_topic():
    topic = manager.create_iot_topic(project_id, topic_id)

    yield topic

    pubsub_client = pubsub.PublisherClient()
    topic_path = pubsub_client.topic_path(project_id, topic_id)
    pubsub_client.delete_topic(topic_path)


def test_image(test_topic, capsys):
    """Send an inage to a device registry"""
    device_id = device_id_template.format('RSA256')
    manager.open_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)

    manager.create_rs256_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, rsa_cert_path)

    sub_topic = 'events'
    mqtt_topic = '/devices/{}/{}'.format(device_id, sub_topic)

    cloudiot_mqtt_image.transmit_image(
        cloud_region, registry_id, device_id, rsa_private_path, ca_cert_path,
        image_path)
