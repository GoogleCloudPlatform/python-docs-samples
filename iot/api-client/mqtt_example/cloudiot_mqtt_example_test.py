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

import pytest

from fixtures import test_topic  # noqa
from fixtures import test_registry_id  # noqa
from fixtures import test_device_id  # noqa
from fixtures import device_and_gateways  # noqa

# Add manager for bootstrapping device registry / device for testing
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "manager"))  # noqa
import cloudiot_mqtt_example  # noqa
import manager  # noqa


cloud_region = "us-central1"
ca_cert_path = "resources/roots.pem"
rsa_private_path = "resources/rsa_private.pem"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
service_account_json = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

mqtt_bridge_hostname = "mqtt.googleapis.com"
mqtt_bridge_port = 443


def test_event(test_topic, test_registry_id, test_device_id, capsys):  # noqa
    manager.get_device(
        service_account_json, project_id, cloud_region, test_registry_id, test_device_id
    )

    sub_topic = "events"
    mqtt_topic = f"/devices/{test_device_id}/{sub_topic}"

    client = cloudiot_mqtt_example.get_client(
        project_id,
        cloud_region,
        test_registry_id,
        test_device_id,
        rsa_private_path,
        "RS256",
        ca_cert_path,
        "mqtt.googleapis.com",
        443,
    )

    client.loop_start()
    client.publish(mqtt_topic, "just test", qos=1)
    time.sleep(2)
    client.loop_stop()

    manager.get_state(
        service_account_json, project_id, cloud_region, test_registry_id, test_device_id
    )

    out, _ = capsys.readouterr()
    assert "on_publish" in out


def test_state(test_topic, test_registry_id, test_device_id, capsys):  # noqa
    manager.get_device(
        service_account_json, project_id, cloud_region, test_registry_id, test_device_id
    )

    sub_topic = "state"
    mqtt_topic = f"/devices/{test_device_id}/{sub_topic}"

    client = cloudiot_mqtt_example.get_client(
        project_id,
        cloud_region,
        test_registry_id,
        test_device_id,
        rsa_private_path,
        "RS256",
        ca_cert_path,
        "mqtt.googleapis.com",
        443,
    )
    client.publish(mqtt_topic, "state test", qos=1)
    client.loop_start()

    time.sleep(3)

    client.loop_stop()

    manager.get_state(
        service_account_json, project_id, cloud_region, test_registry_id, test_device_id
    )

    out, _ = capsys.readouterr()
    assert "on_publish" in out
    assert 'binary_data: "state test"' in out


def test_config(test_topic, test_registry_id, test_device_id, capsys):  # noqa
    manager.get_device(
        service_account_json, project_id, cloud_region, test_registry_id, test_device_id
    )

    client = cloudiot_mqtt_example.get_client(
        project_id,
        cloud_region,
        test_registry_id,
        test_device_id,
        rsa_private_path,
        "RS256",
        ca_cert_path,
        "mqtt.googleapis.com",
        443,
    )
    client.loop_start()

    time.sleep(5)

    client.loop_stop()

    manager.get_state(
        service_account_json, project_id, cloud_region, test_registry_id, test_device_id
    )

    out, _ = capsys.readouterr()
    assert "Received message" in out
    assert f"/devices/{test_device_id}/config" in out


@pytest.mark.flaky(max_runs=5, min_passes=1)
def test_receive_command(test_registry_id, test_device_id, capsys):  # noqa
    # Exercize the functionality
    client = cloudiot_mqtt_example.get_client(
        project_id,
        cloud_region,
        test_registry_id,
        test_device_id,
        rsa_private_path,
        "RS256",
        ca_cert_path,
        "mqtt.googleapis.com",
        443,
    )
    client.loop_start()

    # Pre-process commands
    for i in range(1, 5):
        client.loop()
        time.sleep(1)

    manager.send_command(
        service_account_json,
        project_id,
        cloud_region,
        test_registry_id,
        test_device_id,
        "me want cookies",
    )

    # Process commands
    for i in range(1, 5):
        client.loop()
        time.sleep(1)

    out, _ = capsys.readouterr()
    assert "on_connect" in out  # Verify can connect
    assert "'me want cookies'" in out  # Verify can receive command


@pytest.mark.flaky(max_runs=5, min_passes=1)
def test_gateway_listen_for_bound_device_configs(
    test_topic, test_registry_id, device_and_gateways, capsys):  # noqa
    (device_id, gateway_id, _) = device_and_gateways

    # Setup for listening for config messages
    num_messages = 0
    jwt_exp_time = 60
    listen_time = 30

    # Connect the gateway
    cloudiot_mqtt_example.listen_for_messages(
        service_account_json,
        project_id,
        cloud_region,
        test_registry_id,
        device_id,
        gateway_id,
        num_messages,
        rsa_private_path,
        "RS256",
        ca_cert_path,
        mqtt_bridge_hostname,
        mqtt_bridge_port,
        jwt_exp_time,
        listen_time,
        None,
    )

    out, _ = capsys.readouterr()
    assert "Received message" in out


@pytest.mark.flaky(max_runs=5, min_passes=1)
def test_gateway_send_data_for_device(
    test_topic, test_registry_id, device_and_gateways, capsys):  # noqa
    (device_id, gateway_id, _) = device_and_gateways

    # Setup for listening for config messages
    num_messages = 5
    jwt_exp_time = 60
    listen_time = 20

    # Connect the gateway
    cloudiot_mqtt_example.send_data_from_bound_device(
        service_account_json,
        project_id,
        cloud_region,
        test_registry_id,
        device_id,
        gateway_id,
        num_messages,
        rsa_private_path,
        "RS256",
        ca_cert_path,
        mqtt_bridge_hostname,
        mqtt_bridge_port,
        jwt_exp_time,
        listen_time,
    )

    out, _ = capsys.readouterr()
    assert "Publishing message 5/5" in out
    assert "Received message" in out


def test_gateway_trigger_error_topic(
    test_topic, test_registry_id, device_and_gateways, capsys):  # noqa
    (device_id, _, gateway_id) = device_and_gateways

    # Setup for listening for config messages
    num_messages = 4

    # Hardcoded callback for causing an error
    def trigger_error(client):
        cloudiot_mqtt_example.attach_device(client, "invalid_device_id", "")

    # Connect the gateway
    cloudiot_mqtt_example.listen_for_messages(
        service_account_json,
        project_id,
        cloud_region,
        test_registry_id,
        device_id,
        gateway_id,
        num_messages,
        rsa_private_path,
        "RS256",
        ca_cert_path,
        "mqtt.googleapis.com",
        443,
        20,
        42,
        trigger_error,
    )
    # Try to connect the gateway aagin on 8883
    cloudiot_mqtt_example.listen_for_messages(
        service_account_json,
        project_id,
        cloud_region,
        test_registry_id,
        device_id,
        gateway_id,
        num_messages,
        rsa_private_path,
        "RS256",
        ca_cert_path,
        "mqtt.googleapis.com",
        8883,
        20,
        15,
        trigger_error,
    )

    out, _ = capsys.readouterr()
    assert "GATEWAY_ATTACHMENT_ERROR" in out
