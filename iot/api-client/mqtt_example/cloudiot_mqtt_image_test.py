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
import os
import sys
import tempfile

# Add manager as library
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "manager"))  # noqa
import cloudiot_mqtt_image  # noqa
import manager  # noqa
from fixtures import test_topic  # noqa
from fixtures import test_subscription  # noqa
from fixtures import test_registry_id  # noqa
from fixtures import test_device_id  # noqa


cloud_region = "us-central1"
ca_cert_path = "resources/roots.pem"
rsa_private_path = "resources/rsa_private.pem"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
service_account_json = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
image_path = "./resources/owlister_hootie.png"


def test_image(test_topic, test_registry_id, test_device_id, capsys):  # noqa
    """Send an inage to a device registry"""
    manager.get_device(
        service_account_json, project_id, cloud_region, test_registry_id, test_device_id
    )

    cloudiot_mqtt_image.transmit_image(
        cloud_region,
        test_registry_id,
        test_device_id,
        rsa_private_path,
        ca_cert_path,
        image_path,
        project_id,
        service_account_json,
    )

    out, _ = capsys.readouterr()
    assert "on_publish" in out


def test_image_recv(
    test_topic,  # noqa
    test_subscription,  # noqa
    test_registry_id,  # noqa
    test_device_id,  # noqa
    capsys,
):
    """Transmit an image with IoT Core and receive it from PubSub"""

    manager.get_device(
        service_account_json, project_id, cloud_region, test_registry_id, test_device_id
    )

    cloudiot_mqtt_image.transmit_image(
        cloud_region,
        test_registry_id,
        test_device_id,
        rsa_private_path,
        ca_cert_path,
        image_path,
        project_id,
        service_account_json,
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        cloudiot_mqtt_image.receive_image(
            project_id, test_subscription.name, tmp_dir + "/test", "png", 120
        )

    out, _ = capsys.readouterr()
    assert "Received image" in out
