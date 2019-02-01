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
from gcp_devrel.testing.flaky import flaky
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

mqtt_bridge_hostname = 'mqtt.googleapis.com'
mqtt_bridge_port = 443


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

    client.loop_start()
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
    client.loop_start()

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
    client.loop_start()

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


@flaky
def test_receive_command(capsys):
    device_id = device_id_template.format('RSA256')
    manager.create_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)

    exists = False
    devices = manager.list_devices(
            service_account_json, project_id, cloud_region, registry_id)
    for device in devices:
        if device.get('id') == device_id:
            exists = True

    if not exists:
        manager.create_rs256_device(
                service_account_json, project_id, cloud_region, registry_id,
                device_id, rsa_cert_path)

    # Exercize the functionality
    client = cloudiot_mqtt_example.get_client(
        project_id, cloud_region, registry_id, device_id,
        rsa_private_path, 'RS256', ca_cert_path,
        'mqtt.googleapis.com', 443)
    client.loop_start()

    # Pre-process commands
    for i in range(1, 5):
        client.loop()
        time.sleep(1)

    manager.send_command(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, 'me want cookies')

    # Process commands
    for i in range(1, 5):
        client.loop()
        time.sleep(1)

    # Clean up
    manager.delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)
    manager.delete_registry(
            service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()
    assert 'on_connect' in out  # Verify can connect
    assert '\'me want cookies\'' in out  # Verify can receive command


@flaky
def test_gateway_listen_for_bound_device_configs(test_topic, capsys):
    gateway_id = device_id_template.format('RS256')
    device_id = device_id_template.format('noauthbind')
    manager.create_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)
    manager.create_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            None, gateway_id, rsa_cert_path, 'RS256')
    manager.create_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)
    manager.bind_device_to_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, gateway_id)

    # Setup for listening for config messages
    num_messages = 0
    jwt_exp_time = 60
    listen_time = 30

    # Connect the gateway
    cloudiot_mqtt_example.listen_for_messages(
                service_account_json, project_id, cloud_region, registry_id,
                device_id, gateway_id, num_messages, rsa_private_path,
                'RS256', ca_cert_path, mqtt_bridge_hostname, mqtt_bridge_port,
                jwt_exp_time, listen_time, None)

    # Clean up
    manager.unbind_device_from_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, gateway_id)
    manager.delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)
    manager.delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            gateway_id)
    manager.delete_registry(
            service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()
    assert 'Received message' in out


def test_gateway_send_data_for_device(test_topic, capsys):
    gateway_id = device_id_template.format('RS256')
    device_id = device_id_template.format('noauthbind')
    manager.create_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)
    manager.create_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            None, gateway_id, rsa_cert_path, 'RS256')
    manager.create_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)
    manager.bind_device_to_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, gateway_id)

    # Setup for listening for config messages
    num_messages = 5
    jwt_exp_time = 60
    listen_time = 20

    # Connect the gateway
    cloudiot_mqtt_example.send_data_from_bound_device(
                service_account_json, project_id, cloud_region, registry_id,
                device_id, gateway_id, num_messages, rsa_private_path,
                'RS256', ca_cert_path, mqtt_bridge_hostname, mqtt_bridge_port,
                jwt_exp_time, listen_time)

    # Clean up
    manager.unbind_device_from_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, gateway_id)
    manager.delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)
    manager.delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            gateway_id)
    manager.delete_registry(
            service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()
    assert 'Publishing message 5/5' in out
    assert 'Out of memory' not in out  # Indicates could not connect


def test_gateway_trigger_error_topic(test_topic, capsys):
    gateway_id = device_id_template.format('RS256-err')
    device_id = device_id_template.format('noauthbind')
    manager.create_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)
    manager.create_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            None, gateway_id, rsa_cert_path, 'RS256')
    manager.create_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)
    manager.bind_device_to_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, gateway_id)

    # Setup for listening for config messages
    num_messages = 4

    # Hardcoded callback for causing an error
    def trigger_error(client):
        cloudiot_mqtt_example.attach_device(client, 'invalid_device_id', '')

    # Connect the gateway
    cloudiot_mqtt_example.listen_for_messages(
                service_account_json, project_id, cloud_region, registry_id,
                device_id, gateway_id, num_messages, rsa_private_path,
                'RS256', ca_cert_path, 'mqtt.googleapis.com', 443,
                20, 15, trigger_error)

    # Clean up
    manager.unbind_device_from_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, gateway_id)
    manager.delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)
    manager.delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            gateway_id)
    manager.delete_registry(
            service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()
    assert 'GATEWAY_ATTACHMENT_ERROR' in out
