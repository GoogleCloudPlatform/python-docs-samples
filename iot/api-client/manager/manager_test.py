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

import manager

import pytest


# TODO: Pull from environment
CLOUD_REGION = 'us-central1'
DEVICE_ID_TEMPLATE = 'test-device-{}'
ES_CERT_PATH = '../ec_public.pem'
RSA_CERT_PATH = '../rsa_cert.pem'
TOPIC_ID = 'test-device-events-{}'.format(int(time.time()))

API_KEY = os.environ['API_KEY']
PROJECT_ID = os.environ['GCLOUD_PROJECT']
SERVICE_ACCOUNT_JSON = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

PUBSUB_TOPIC = 'projects/{}/topics/{}'.format(PROJECT_ID, TOPIC_ID)
REGISTRY_ID = 'test-registry-{}'.format(int(time.time()))


@pytest.fixture(scope='module')
def test_topic():
    topic = manager.create_iot_topic(TOPIC_ID)

    yield topic

    if topic.exists():
        topic.delete()


def test_create_delete_registry(test_topic, capsys):
    manager.open_registry(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            PUBSUB_TOPIC, REGISTRY_ID)

    manager.list_devices(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID)

    out, _ = capsys.readouterr()

    # Check that create / list worked
    assert 'Created registry' in out
    assert 'eventNotificationConfig' in out

    # Clean up
    manager.delete_registry(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID)


def test_add_delete_unauth_device(test_topic, capsys):
    device_id = DEVICE_ID_TEMPLATE.format('UNAUTH')
    manager.open_registry(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            PUBSUB_TOPIC, REGISTRY_ID)

    manager.create_unauth_device(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID, device_id)

    manager.get_device(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID, device_id)

    manager.delete_device(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID, device_id)

    out, _ = capsys.readouterr()
    assert 'UNAUTH' in out


def test_add_delete_rs256_device(test_topic, capsys):
    device_id = DEVICE_ID_TEMPLATE.format('RSA256')
    manager.open_registry(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            PUBSUB_TOPIC, REGISTRY_ID)

    manager.create_rs256_device(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID, device_id, RSA_CERT_PATH)

    manager.get_device(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID, device_id)

    manager.delete_device(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID, device_id)

    manager.delete_registry(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID)

    out, _ = capsys.readouterr()
    assert 'format : RSA_X509_PEM' in out


def test_add_delete_es256_device(test_topic, capsys):
    device_id = DEVICE_ID_TEMPLATE.format('ES256')
    manager.open_registry(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            PUBSUB_TOPIC, REGISTRY_ID)

    manager.create_es256_device(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID, device_id, ES_CERT_PATH)

    manager.get_device(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID, device_id)

    manager.delete_device(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID, device_id)

    manager.delete_registry(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID)

    out, _ = capsys.readouterr()
    assert 'format : ES256_PEM' in out


def test_add_patch_delete_rs256(test_topic, capsys):
    device_id = DEVICE_ID_TEMPLATE.format('PATCHME')
    manager.open_registry(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            PUBSUB_TOPIC, REGISTRY_ID)

    manager.create_rs256_device(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID, device_id, RSA_CERT_PATH)

    manager.get_device(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID, device_id)
    out, _ = capsys.readouterr()
    assert 'format : RSA_X509_PEM' in out

    manager.patch_es256_auth(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID, device_id, ES_CERT_PATH)

    manager.get_device(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID, device_id)
    out, _ = capsys.readouterr()
    assert 'format : ES256_PEM' in out

    manager.delete_device(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID, device_id)

    manager.delete_registry(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID)


def test_add_patch_delete_es256(test_topic, capsys):
    device_id = DEVICE_ID_TEMPLATE.format('PATCHME')
    manager.open_registry(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            PUBSUB_TOPIC, REGISTRY_ID)

    manager.create_es256_device(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID, device_id, ES_CERT_PATH)

    manager.get_device(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID, device_id)
    out, _ = capsys.readouterr()
    assert 'format : ES256_PEM' in out

    manager.patch_rsa256_auth(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID, device_id, RSA_CERT_PATH)

    manager.get_device(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID, device_id)
    out, _ = capsys.readouterr()
    assert 'format : RSA_X509_PEM' in out

    manager.delete_device(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID, device_id)

    manager.delete_registry(
            SERVICE_ACCOUNT_JSON, API_KEY, PROJECT_ID, CLOUD_REGION,
            REGISTRY_ID)
