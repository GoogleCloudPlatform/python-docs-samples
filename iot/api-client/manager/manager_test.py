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

import pytest

import manager


cloud_region = 'us-central1'
device_id_template = 'test-device-{}'
es_cert_path = 'resources/ec_public.pem'
rsa_cert_path = 'resources/rsa_cert.pem'
topic_id = 'test-device-events-{}'.format(int(time.time()))

project_id = os.environ['GCLOUD_PROJECT']
service_account_json = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

pubsub_topic = 'projects/{}/topics/{}'.format(project_id, topic_id)
registry_id = 'test-registry-{}'.format(int(time.time()))


@pytest.fixture(scope='module')
def test_topic():
    topic = manager.create_iot_topic(topic_id)

    yield topic

    if topic.exists():
        topic.delete()


def test_create_delete_registry(test_topic, capsys):
    manager.open_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)

    manager.list_devices(
            service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()

    # Check that create / list worked
    assert 'Created registry' in out
    assert 'eventNotificationConfig' in out

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

    out, _ = capsys.readouterr()
    assert 'UNAUTH' in out


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
    assert 'State: {' in out


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
    assert 'State: {' in out


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
