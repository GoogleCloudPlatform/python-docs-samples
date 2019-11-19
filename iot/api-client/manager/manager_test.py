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

import datetime
import os
import sys
import time

# Add command receiver for bootstrapping device registry / device for testing
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mqtt_example'))  # noqa
from gcp_devrel.testing.flaky import flaky
from google.cloud import pubsub
import pytest

import manager
import cloudiot_mqtt_example

cloud_region = 'us-central1'
device_id_template = 'test-device-{}'
ca_cert_path = '../mqtt_example/resources/roots.pem'
es_cert_path = 'resources/ec_public.pem'
rsa_cert_path = 'resources/rsa_cert.pem'
rsa_private_path = 'resources/rsa_private.pem'  # Must match rsa_cert
topic_id = 'test-device-events-{}'.format(int(time.time()))

project_id = os.environ['GCLOUD_PROJECT']
service_account_json = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

pubsub_topic = 'projects/{}/topics/{}'.format(project_id, topic_id)
registry_id = 'test-registry-{}'.format(int(time.time()))


@pytest.fixture(scope="session", autouse=True)
def clean_up_registries():
    all_registries = list(manager.list_registries(
        service_account_json, project_id, cloud_region))

    for registry in all_registries:
        registry_id = registry.id
        if registry_id.find('test-registry-') == 0:
            time_str = registry_id[
                registry_id.rfind('-') + 1: len(registry_id)]
            test_date = datetime.datetime.utcfromtimestamp(int(time_str))
            now_date = datetime.datetime.utcfromtimestamp(int(time.time()))
            difftime = now_date - test_date

            # *NOTE* Restrict to registries used in the tests older than 30
            #        days to prevent thrashing in the case of async tests
            if (difftime.days > 30):
                client = manager.get_client(service_account_json)
                gateways = client.projects().locations().registries().devices(
                    ).list(
                        parent=registry.name,
                        fieldMask='config,gatewayConfig'
                    ).execute().get('devices', [])
                devices = client.projects().locations().registries().devices(
                    ).list(parent=registry.name).execute().get(
                        'devices', [])

                # Unbind devices from each gateway and delete
                for gateway in gateways:
                    gateway_id = gateway.get('id')
                    bound = client.projects().locations().registries().devices(
                        ).list(
                            parent=registry.name,
                            gatewayListOptions_associationsGatewayId=gateway_id
                        ).execute()
                    if 'devices' in bound:
                        for device in bound['devices']:
                            bind_request = {
                                'deviceId': device.get('id'),
                                'gatewayId': gateway_id
                            }
                            client.projects().locations().registries(
                                ).unbindDeviceFromGateway(
                                    parent=registry.get('name'),
                                    body=bind_request).execute()
                    gateway_name = '{}/devices/{}'.format(
                        registry.name, gateway_id)
                    client.projects().locations().registries().devices(
                        ).delete(name=gateway_name).execute()

                # Delete the devices
                # Assumption is that the devices are not bound to gateways
                for device in devices:
                    device_name = '{}/devices/{}'.format(
                        registry.name, device.get('id'))
                    print(device_name)
                    remove_device = True
                    try:
                        client.projects().locations().registries().devices(
                            ).get(name=device_name).execute()
                    except Exception:
                        remove_device = False

                    if remove_device:
                        print('removing {}'.format(device_name))
                        client.projects().locations().registries().devices(
                            ).delete(name=device_name).execute()

                # Delete the old test registry
                client.projects().locations().registries().delete(
                    name=registry.name).execute()


@pytest.fixture(scope='module')
def test_topic():
    topic = manager.create_iot_topic(project_id, topic_id)

    yield topic

    pubsub_client = pubsub.PublisherClient()
    topic_path = pubsub_client.topic_path(project_id, topic_id)
    pubsub_client.delete_topic(topic_path)


def test_create_delete_registry(test_topic, capsys):
    manager.open_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)

    manager.list_devices(
            service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()

    # Check that create / list worked
    assert 'Created registry' in out
    assert 'event_notification_config' in out

    # Clean up
    manager.delete_registry(
            service_account_json, project_id, cloud_region, registry_id)


def test_get_iam_permissions(test_topic, capsys):
    manager.open_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)

    manager.list_devices(
            service_account_json, project_id, cloud_region, registry_id)

    # Test getting IAM permissions
    print(manager.get_iam_permissions(
            service_account_json, project_id, cloud_region, registry_id))

    # Test setting IAM permissions
    MEMBER = "group:dpebot@google.com"
    ROLE = "roles/viewer"
    print(manager.set_iam_permissions(
            service_account_json, project_id, cloud_region, registry_id,
            ROLE, MEMBER))

    out, _ = capsys.readouterr()

    # Check that create / list worked
    assert 'Created registry' in out
    assert 'event_notification_config' in out
    assert 'dpebot' in out
    assert 'etag' in out

    # Clean up
    manager.delete_registry(
            service_account_json, project_id, cloud_region, registry_id)


def test_add_delete_unauth_device(test_topic, capsys):
    device_id = device_id_template.format('UNAUTH')
    manager.open_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)

    manager.create_unauth_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    manager.get_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    manager.delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    manager.delete_registry(
            service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()
    assert 'UNAUTH' in out


def test_add_config_unauth_device(test_topic, capsys):
    device_id = device_id_template.format('UNAUTH')
    manager.open_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)

    manager.create_unauth_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    manager.set_config(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, 0, 'test')

    manager.get_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    manager.get_config_versions(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    manager.delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    manager.delete_registry(
            service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()
    assert 'Set device configuration' in out
    assert 'UNAUTH' in out
    assert 'version: 2' in out


def test_add_delete_rs256_device(test_topic, capsys):
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

    manager.get_state(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    manager.delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    manager.delete_registry(
            service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()
    assert 'format : RSA_X509_PEM' in out


def test_add_delete_es256_device(test_topic, capsys):
    device_id = device_id_template.format('ES256')
    manager.open_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)

    manager.create_es256_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, es_cert_path)

    manager.get_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    manager.get_state(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    manager.delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    manager.delete_registry(
            service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()
    assert 'format : ES256_PEM' in out


def test_add_patch_delete_rs256(test_topic, capsys):
    device_id = device_id_template.format('PATCHME')
    manager.open_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)

    manager.create_rs256_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, rsa_cert_path)

    manager.get_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)
    out, _ = capsys.readouterr()
    assert 'format : RSA_X509_PEM' in out

    manager.patch_es256_auth(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, es_cert_path)

    manager.get_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)
    out, _ = capsys.readouterr()
    assert 'format : ES256_PEM' in out

    manager.delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    manager.delete_registry(
            service_account_json, project_id, cloud_region, registry_id)


def test_add_patch_delete_es256(test_topic, capsys):
    device_id = device_id_template.format('PATCHME')
    manager.open_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)

    manager.create_es256_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, es_cert_path)

    manager.get_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)
    out, _ = capsys.readouterr()
    assert 'format : ES256_PEM' in out

    manager.patch_rsa256_auth(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, rsa_cert_path)

    manager.get_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)
    out, _ = capsys.readouterr()
    assert 'format : RSA_X509_PEM' in out

    manager.delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    manager.delete_registry(
            service_account_json, project_id, cloud_region, registry_id)


@flaky
def test_send_command(test_topic, capsys):
    device_id = device_id_template.format('RSA256')
    manager.create_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)

    exists = False
    devices = manager.list_devices(
            service_account_json, project_id, cloud_region, registry_id)
    for device in devices:
        if device.id == device_id:
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
    out, _ = capsys.readouterr()

    # Pre-process commands
    for i in range(1, 5):
        client.loop()
        time.sleep(1)

    manager.send_command(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, 'me want cookies')
    out, _ = capsys.readouterr()

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

    assert 'Sending command to device' in out
    assert '400' not in out


def test_create_gateway(test_topic, capsys):
    gateway_id = device_id_template.format('RS256')
    manager.create_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)

    # TODO: consider adding test for ES256
    manager.create_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            None, gateway_id, rsa_cert_path, 'RS256')

    # Clean up
    manager.delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            gateway_id)
    manager.delete_registry(
            service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()

    assert 'Created Gateway' in out


def test_list_gateways(test_topic, capsys):
    gateway_id = device_id_template.format('RS256')
    manager.create_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)

    # TODO: consider adding test for ES256
    manager.create_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            None, gateway_id, rsa_cert_path, 'RS256')

    manager.list_gateways(
        service_account_json, project_id, cloud_region, registry_id)

    # Clean up
    manager.delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            gateway_id)
    manager.delete_registry(
            service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()

    assert 'Gateway ID: {}'.format(gateway_id) in out


def test_bind_device_to_gateway_and_unbind(test_topic, capsys):
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
    manager.unbind_device_from_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, gateway_id)

    # Clean up
    manager.delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)
    manager.delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            gateway_id)
    manager.delete_registry(
            service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()

    assert 'Device Bound' in out
    assert 'Device unbound' in out
    assert 'HttpError 404' not in out
