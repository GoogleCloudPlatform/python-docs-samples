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
import sys
import time

from google.cloud import pubsub

# Add manager for bootstrapping device registry / device for testing
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'manager'))  # noqa
import manager

import pytest

import cloudiot_mqtt_example


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


@pytest.fixture(scope='module')
def test_topic():
    topic = manager.create_iot_topic(project_id, topic_id)

    yield topic

    pubsub_client = pubsub.PublisherClient()
    topic_path = pubsub_client.topic_path(project_id, topic_id)
    pubsub_client.delete_topic(topic_path)


def test_event(test_topic, capsys):
    device_id = device_id_template.format('RSA256')
    manager.open_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)

    manager.create_rs256_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, rsa_cert_path)

    manager.get_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    sub_topic = 'events'
    mqtt_topic = '/devices/{}/{}'.format(device_id, sub_topic)

    client = cloudiot_mqtt_example.get_client(
        project_id, cloud_region, registry_id, device_id,
        rsa_private_path, 'RS256', ca_cert_path,
        'mqtt.googleapis.com', 443)

    client.publish(mqtt_topic, 'just test', qos=1)
    time.sleep(2)
    client.loop_stop()

    manager.get_state(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    manager.delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    manager.delete_registry(
            service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()
    assert 'on_publish' in out


def test_state(test_topic, capsys):
    device_id = device_id_template.format('RSA256')
    manager.open_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)

    manager.create_rs256_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, rsa_cert_path)

    manager.get_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    sub_topic = 'state'
    mqtt_topic = '/devices/{}/{}'.format(device_id, sub_topic)

    client = cloudiot_mqtt_example.get_client(
        project_id, cloud_region, registry_id, device_id,
        rsa_private_path, 'RS256', ca_cert_path,
        'mqtt.googleapis.com', 443)
    client.publish(mqtt_topic, 'state test', qos=1)
    time.sleep(3)
    client.loop_stop()

    manager.get_state(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    manager.delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    manager.delete_registry(
            service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()
    assert 'on_publish' in out
    assert 'c3RhdGUgdGVzdA' in out


def test_config(test_topic, capsys):
    device_id = device_id_template.format('RSA256')
    manager.open_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)

    manager.create_rs256_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, rsa_cert_path)

    manager.get_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    client = cloudiot_mqtt_example.get_client(
        project_id, cloud_region, registry_id, device_id,
        rsa_private_path, 'RS256', ca_cert_path,
        'mqtt.googleapis.com', 443)
    time.sleep(5)
    client.loop_stop()

    manager.get_state(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    manager.delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    manager.delete_registry(
            service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()
    assert "Received message" in out
    assert '/devices/{}/config'.format(device_id) in out
