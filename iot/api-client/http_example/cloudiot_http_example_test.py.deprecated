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
import uuid

from google.cloud import pubsub
import pytest

import cloudiot_http_example

# Add manager for bootstrapping device registry / device for testing
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "manager"))  # noqa
import manager  # noqa


cloud_region = "us-central1"
device_id_template = "test-device-{}"
es_cert_path = "resources/ec_public.pem"
rsa_cert_path = "resources/rsa_cert.pem"
rsa_private_path = "resources/rsa_private.pem"
topic_id = f"test-device-events-topic-{int(time.time())}"

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
service_account_json = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

pubsub_topic = f"projects/{project_id}/topics/{topic_id}"
registry_id = f"test-registry-{uuid.uuid4().hex}-{int(time.time())}"

_BASE_URL = "https://cloudiotdevice.googleapis.com/v1"


@pytest.fixture(scope="module")
def test_topic():
    topic = manager.create_iot_topic(project_id, topic_id)

    yield topic

    pubsub_client = pubsub.PublisherClient()
    topic_path = pubsub_client.topic_path(project_id, topic_id)
    pubsub_client.delete_topic(request={"topic": topic_path})


def test_event(test_topic, capsys):
    device_id = device_id_template.format("RSA256")
    manager.open_registry(
        service_account_json, project_id, cloud_region, pubsub_topic, registry_id
    )

    manager.create_rs256_device(
        service_account_json,
        project_id,
        cloud_region,
        registry_id,
        device_id,
        rsa_cert_path,
    )

    manager.get_device(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )

    jwt_token = cloudiot_http_example.create_jwt(
        project_id, "resources/rsa_private.pem", "RS256"
    )

    print(
        cloudiot_http_example.publish_message(
            "hello",
            "event",
            _BASE_URL,
            project_id,
            cloud_region,
            registry_id,
            device_id,
            jwt_token,
        )
    )

    manager.delete_device(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )

    manager.delete_registry(service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()
    assert "format : RSA_X509_PEM" in out
    assert "200" in out


def test_state(test_topic, capsys):
    device_id = device_id_template.format("RSA256")
    manager.open_registry(
        service_account_json, project_id, cloud_region, pubsub_topic, registry_id
    )

    manager.create_rs256_device(
        service_account_json,
        project_id,
        cloud_region,
        registry_id,
        device_id,
        rsa_cert_path,
    )

    manager.get_device(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )

    jwt_token = cloudiot_http_example.create_jwt(
        project_id, "resources/rsa_private.pem", "RS256"
    )

    print(
        cloudiot_http_example.publish_message(
            "hello",
            "state",
            _BASE_URL,
            project_id,
            cloud_region,
            registry_id,
            device_id,
            jwt_token,
        )
    )

    manager.get_state(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )

    manager.delete_device(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )

    manager.delete_registry(service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()
    assert "format : RSA_X509_PEM" in out
    assert 'binary_data: "hello"' in out
    assert "200" in out


def test_config(test_topic, capsys):
    device_id = device_id_template.format("RSA256")
    manager.open_registry(
        service_account_json, project_id, cloud_region, pubsub_topic, registry_id
    )

    manager.create_rs256_device(
        service_account_json,
        project_id,
        cloud_region,
        registry_id,
        device_id,
        rsa_cert_path,
    )

    manager.get_device(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )

    jwt_token = cloudiot_http_example.create_jwt(
        project_id, "resources/rsa_private.pem", "RS256"
    )

    print(
        cloudiot_http_example.get_config(
            "0",
            "state",
            _BASE_URL,
            project_id,
            cloud_region,
            registry_id,
            device_id,
            jwt_token,
        ).text
    )

    manager.get_state(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )

    manager.delete_device(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )

    manager.delete_registry(service_account_json, project_id, cloud_region, registry_id)

    out, _ = capsys.readouterr()
    assert "format : RSA_X509_PEM" in out
    assert '"version": "1"' in out
