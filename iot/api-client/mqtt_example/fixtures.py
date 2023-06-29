# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
#
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

import backoff
from google.api_core.exceptions import AlreadyExists
from google.api_core.exceptions import NotFound
from google.cloud import pubsub
from googleapiclient.errors import HttpError
import pytest

# Add manager as library
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "manager"))  # noqa
import manager  # noqa


cloud_region = "us-central1"
device_id_template = "test-device-{}"
rsa_cert_path = "resources/rsa_cert.pem"
topic_id = f"test-device-events-topic-{uuid.uuid4()}"
subscription_name = f"test-device-images-{uuid.uuid4()}"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
service_account_json = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
registry_id = f"test-registry-{uuid.uuid4().hex}-{int(time.time())}"


@pytest.fixture(scope="session")
def test_topic():
    pubsub_client = pubsub.PublisherClient()
    try:
        topic = manager.create_iot_topic(project_id, topic_id)
    except AlreadyExists as e:
        print(f"The topic already exists, detail: {str(e)}")
        # Ignore the error, fetch the topic
        topic = pubsub_client.get_topic(
            request={"topic": pubsub_client.topic_path(project_id, topic_id)}
        )

    yield topic

    topic_path = pubsub_client.topic_path(project_id, topic_id)
    try:
        pubsub_client.delete_topic(request={"topic": topic_path})
    except NotFound as e:
        # We ignore this case.
        print(f"The topic doesn't exist: detail: {str(e)}")


@pytest.fixture(scope="session")
def test_subscription(test_topic):
    subscriber = pubsub.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    try:
        subscription = subscriber.create_subscription(
            request={"name": subscription_path, "topic": test_topic.name}
        )
    except AlreadyExists as e:
        print(f"The topic already exists, detail: {str(e)}")
        # Ignore the error, fetch the subscription
        subscription = subscriber.get_subscription(
            request={"subscription": subscription_path}
        )

    yield subscription

    try:
        subscriber.delete_subscription(request={"subscription": subscription_path})
    except NotFound as e:
        # We ignore this case.
        print(f"The subscription doesn't exist: detail: {str(e)}")


@pytest.fixture(scope="session")
def test_registry_id(test_topic):
    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def create_registry():
        manager.open_registry(
            service_account_json, project_id, cloud_region, test_topic.name, registry_id
        )

    create_registry()

    yield registry_id

    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def delete_registry():
        try:
            manager.delete_registry(
                service_account_json, project_id, cloud_region, registry_id
            )
        except NotFound as e:
            # We ignore this case.
            print(f"The registry doesn't exist: detail: {str(e)}")

    delete_registry()


@pytest.fixture(scope="session")
def test_device_id(test_registry_id):
    device_id = device_id_template.format("RSA256")

    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def create_device():
        try:
            manager.create_rs256_device(
                service_account_json,
                project_id,
                cloud_region,
                test_registry_id,
                device_id,
                rsa_cert_path,
            )
        except AlreadyExists as e:
            # We ignore this case.
            print(f"The device already exists: detail: {str(e)}")

    create_device()

    yield device_id

    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def delete_device():
        try:
            manager.delete_device(
                service_account_json,
                project_id,
                cloud_region,
                test_registry_id,
                device_id,
            )
        except NotFound as e:
            # We ignore this case.
            print(f"The device doesn't exist: detail: {str(e)}")

    delete_device()


@pytest.fixture(scope="module")
def device_and_gateways(test_registry_id):
    device_id = device_id_template.format("noauthbind")
    gateway_id = device_id_template.format("RS256")
    bad_gateway_id = device_id_template.format("RS256-err")

    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def create_device():
        manager.create_device(
            service_account_json, project_id, cloud_region, test_registry_id, device_id
        )

    create_device()

    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def create_gateways():
        manager.create_gateway(
            service_account_json,
            project_id,
            cloud_region,
            test_registry_id,
            None,
            gateway_id,
            rsa_cert_path,
            "RS256",
        )
        manager.create_gateway(
            service_account_json,
            project_id,
            cloud_region,
            test_registry_id,
            None,
            bad_gateway_id,
            rsa_cert_path,
            "RS256",
        )

    create_gateways()

    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def bind_device_to_gateways():
        manager.bind_device_to_gateway(
            service_account_json,
            project_id,
            cloud_region,
            test_registry_id,
            device_id,
            gateway_id,
        )
        manager.bind_device_to_gateway(
            service_account_json,
            project_id,
            cloud_region,
            test_registry_id,
            device_id,
            bad_gateway_id,
        )

    bind_device_to_gateways()

    yield (device_id, gateway_id, bad_gateway_id)

    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def unbind():
        manager.unbind_device_from_gateway(
            service_account_json,
            project_id,
            cloud_region,
            test_registry_id,
            device_id,
            gateway_id,
        )
        manager.unbind_device_from_gateway(
            service_account_json,
            project_id,
            cloud_region,
            test_registry_id,
            device_id,
            bad_gateway_id,
        )

    unbind()

    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def delete_device():
        try:
            manager.delete_device(
                service_account_json,
                project_id,
                cloud_region,
                test_registry_id,
                device_id,
            )
        except NotFound as e:
            # We ignore this case.
            print(f"The device doesn't exist: detail: {str(e)}")

    delete_device()

    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def delete_gateways():
        try:
            manager.delete_device(
                service_account_json,
                project_id,
                cloud_region,
                test_registry_id,
                gateway_id,
            )
        except NotFound as e:
            # We ignore this case.
            print(f"The gateway doesn't exist: detail: {str(e)}")
        try:
            manager.delete_device(
                service_account_json,
                project_id,
                cloud_region,
                test_registry_id,
                bad_gateway_id,
            )
        except NotFound as e:
            # We ignore this case.
            print(f"The gateway doesn't exist: detail: {str(e)}")

    delete_gateways()
