# Copyright 2018 Google LLC
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
import io
import os
import sys
import time

# Add command receiver for bootstrapping device registry / device for testing
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'receive'))  # noqa
from google.cloud import pubsub
import pytest

import gateway

cloud_region = 'us-central1'
device_id_template = 'test-device-{}'
gateway_id_template = 'test-gateway-{}'
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


# TODO: Remove once possible
def create_iot_topic(project, topic_name):
    """Creates a PubSub Topic and grants access to Cloud IoT Core."""
    pubsub_client = pubsub.PublisherClient()
    topic_path = pubsub_client.topic_path(project, topic_name)

    topic = pubsub_client.create_topic(topic_path)
    policy = pubsub_client.get_iam_policy(topic_path)

    policy.bindings.add(
        role='roles/pubsub.publisher',
        members=['serviceAccount:cloud-iot@system.gserviceaccount.com'])

    pubsub_client.set_iam_policy(topic_path, policy)

    return topic


def create_registry(
        service_account_json, project_id, cloud_region, pubsub_topic,
        registry_id):
    """ Creates a registry and returns the result. Returns an empty result if
    the registry already exists."""
    client = gateway.get_client(service_account_json)
    registry_parent = 'projects/{}/locations/{}'.format(
            project_id,
            cloud_region)
    body = {
        'eventNotificationConfigs': [{
            'pubsubTopicName': pubsub_topic
        }],
        'id': registry_id
    }
    request = client.projects().locations().registries().create(
        parent=registry_parent, body=body)

    response = request.execute()
    print('Created registry')
    return response


def delete_registry(
       service_account_json, project_id, cloud_region, registry_id):
    """Deletes the specified registry."""
    print('Delete registry')
    client = gateway.get_client(service_account_json)
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    registries = client.projects().locations().registries()
    return registries.delete(name=registry_name).execute()


def create_device(
        service_account_json, project_id, cloud_region, registry_id,
        device_id, certificate_file):
    """Create a new device without authentication."""
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    with io.open(certificate_file) as f:
        certificate = f.read()

    client = gateway.get_client(service_account_json)
    device_template = {
        'id': device_id,
        'credentials': [{
            'publicKey': {
                'format': 'RSA_X509_PEM',
                'key': certificate
            }
        }]
    }

    devices = client.projects().locations().registries().devices()
    return devices.create(parent=registry_name, body=device_template).execute()


def delete_device(
        service_account_json, project_id, cloud_region, registry_id,
        device_id):
    """Delete the device with the given id."""
    print('Delete device')
    client = gateway.get_client(service_account_json)
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    device_name = '{}/devices/{}'.format(registry_name, device_id)

    devices = client.projects().locations().registries().devices()
    return devices.delete(name=device_name).execute()


# Keep scaffolding from here
@pytest.fixture(scope='module')
def iot_topic():
    topic = create_iot_topic(project_id, topic_id)

    yield topic

    pubsub_client = pubsub.PublisherClient()
    topic_path = pubsub_client.topic_path(project_id, topic_id)
    pubsub_client.delete_topic(topic_path)


def test_create_gateway(iot_topic, capsys):
    gateway_id = device_id_template.format('RS256')
    create_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)

    # TODO: consider adding test for ES256
    gateway.create_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            None, gateway_id, rsa_cert_path, 'RS256')

    # Clean up
    delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            gateway_id)
    delete_registry(
            service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()

    assert 'Created gateway' in out


def test_list_gateways(iot_topic, capsys):
    gateway_id = device_id_template.format('RS256')
    create_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)

    # TODO: consider adding test for ES256
    gateway.create_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            None, gateway_id, rsa_cert_path, 'RS256')

    gateway.list_gateways(
        service_account_json, project_id, cloud_region, registry_id)

    # Clean up
    delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            gateway_id)
    delete_registry(
            service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()

    assert 'Gateway ID: {}'.format(gateway_id) in out


def test_bind_device_to_gateway_and_unbind(iot_topic, capsys):
    gateway_id = device_id_template.format('RS256')
    device_id = device_id_template.format('noauthbind')
    create_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)
    gateway.create_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            None, gateway_id, rsa_cert_path, 'RS256')

    gateway.create_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    gateway.bind_device_to_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, gateway_id)
    gateway.unbind_device_from_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, gateway_id)

    # Clean up
    delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)
    delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            gateway_id)
    delete_registry(
            service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()

    assert 'Device Bound' in out
    assert 'Device unbound' in out
    assert 'HttpError 404' not in out


def test_gateway_listen_for_bound_device_configs(iot_topic, capsys):
    gateway_id = device_id_template.format('RS256')
    device_id = device_id_template.format('noauthbind')
    create_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)
    gateway.create_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            None, gateway_id, rsa_cert_path, 'RS256')
    gateway.create_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)
    gateway.bind_device_to_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, gateway_id)

    # Setup for listening for config messages
    num_messages = 0
    jwt_exp_time = 60
    listen_time = 30

    # Connect the gateway
    gateway.listen_for_config_and_error_messages(
                service_account_json, project_id, cloud_region, registry_id,
                device_id, gateway_id, num_messages, rsa_private_path,
                'RS256', ca_cert_path, mqtt_bridge_hostname, mqtt_bridge_port,
                jwt_exp_time, listen_time, None)

    # Clean up
    gateway.unbind_device_from_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, gateway_id)
    delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)
    delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            gateway_id)
    delete_registry(
            service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()
    assert 'Received message' in out


def test_gateway_send_data_for_device(iot_topic, capsys):
    gateway_id = device_id_template.format('RS256')
    device_id = device_id_template.format('noauthbind')
    create_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)
    gateway.create_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            None, gateway_id, rsa_cert_path, 'RS256')
    gateway.create_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)
    gateway.bind_device_to_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, gateway_id)

    # Setup for listening for config messages
    num_messages = 5
    jwt_exp_time = 60
    listen_time = 20

    # Connect the gateway
    gateway.send_data_from_bound_device(
                service_account_json, project_id, cloud_region, registry_id,
                device_id, gateway_id, num_messages, rsa_private_path,
                'RS256', ca_cert_path, mqtt_bridge_hostname, mqtt_bridge_port,
                jwt_exp_time, listen_time)

    # Clean up
    gateway.unbind_device_from_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, gateway_id)
    delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)
    delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            gateway_id)
    delete_registry(
            service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()
    assert 'Publishing message 5/5' in out
    assert 'Out of memory' not in out  # Indicates could not connect


def test_gateway_trigger_error_topic(iot_topic, capsys):
    gateway_id = device_id_template.format('RS256-err')
    device_id = device_id_template.format('noauthbind')
    create_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)
    gateway.create_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            None, gateway_id, rsa_cert_path, 'RS256')
    gateway.create_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)
    gateway.bind_device_to_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, gateway_id)

    # Setup for listening for config messages
    num_messages = 4
    jwt_exp_time = 30
    listen_time = 5

    # Callback for causing an error
    def trigger_error(client):
        gateway.attach_device(client, 'invalid_device_id')

    # Connect the gateway
    # Connect the gateway
    gateway.listen_for_config_and_error_messages(
                service_account_json, project_id, cloud_region, registry_id,
                device_id, gateway_id, num_messages, rsa_private_path,
                'RS256', ca_cert_path, mqtt_bridge_hostname, mqtt_bridge_port,
                jwt_exp_time, listen_time, trigger_error)

    # Clean up
    gateway.unbind_device_from_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, gateway_id)
    delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)
    delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            gateway_id)
    delete_registry(
            service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()
    assert 'Received ERROR message' in out
    assert 'Out of memory' not in out  # Indicates could not connect
