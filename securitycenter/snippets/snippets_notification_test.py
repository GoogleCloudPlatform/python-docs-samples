#!/usr/bin/env python
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for snippets."""

import os
import uuid

from google.cloud import securitycenter as securitycenter
import pytest

import snippets_notification_configs
import snippets_notification_receiver

ORG_ID = os.environ["GCLOUD_ORGANIZATION"]
PROJECT_ID = os.environ["GCLOUD_PROJECT"]
PUBSUB_TOPIC = os.environ["GCLOUD_PUBSUB_TOPIC"]
PUBSUB_SUBSCRIPTION = os.environ["GCLOUD_PUBSUB_SUBSCRIPTION"]

CREATE_CONFIG_ID = "new-notification-pytest" + str(uuid.uuid1())
DELETE_CONFIG_ID = "new-notification-pytest" + str(uuid.uuid1())
GET_CONFIG_ID = "new-notification-pytest" + str(uuid.uuid1())
UPDATE_CONFIG_ID = "new-notification-pytest" + str(uuid.uuid1())


def cleanup_notification_config(notification_config_id):
    client = securitycenter.SecurityCenterClient()

    notification_config_name = (
        "organizations/{org_id}/notificationConfigs/{config_id}".format(
            org_id=ORG_ID, config_id=notification_config_id
        )
    )
    client.delete_notification_config(request={"name": notification_config_name})


@pytest.fixture
def new_notification_config_for_update():
    client = securitycenter.SecurityCenterClient()

    org_name = "organizations/{org_id}".format(org_id=ORG_ID)

    created_notification_config = client.create_notification_config(
        request={
            "parent": org_name,
            "config_id": UPDATE_CONFIG_ID,
            "notification_config": {
                "description": "Notification for active findings",
                "pubsub_topic": PUBSUB_TOPIC,
                "streaming_config": {"filter": ""},
            },
        }
    )
    yield created_notification_config
    cleanup_notification_config(UPDATE_CONFIG_ID)


@pytest.fixture
def new_notification_config_for_get():
    client = securitycenter.SecurityCenterClient()

    org_name = "organizations/{org_id}".format(org_id=ORG_ID)

    created_notification_config = client.create_notification_config(
        request={
            "parent": org_name,
            "config_id": GET_CONFIG_ID,
            "notification_config": {
                "description": "Notification for active findings",
                "pubsub_topic": PUBSUB_TOPIC,
                "streaming_config": {"filter": ""},
            },
        }
    )
    yield created_notification_config
    cleanup_notification_config(GET_CONFIG_ID)


@pytest.fixture
def deleted_notification_config():
    client = securitycenter.SecurityCenterClient()

    org_name = "organizations/{org_id}".format(org_id=ORG_ID)

    created_notification_config = client.create_notification_config(
        request={
            "parent": org_name,
            "config_id": DELETE_CONFIG_ID,
            "notification_config": {
                "description": "Notification for active findings",
                "pubsub_topic": PUBSUB_TOPIC,
                "streaming_config": {"filter": ""},
            },
        }
    )
    return created_notification_config


def test_create_notification_config():
    created_notification_config = (
        snippets_notification_configs.create_notification_config(
            ORG_ID, CREATE_CONFIG_ID, PUBSUB_TOPIC
        )
    )
    assert created_notification_config is not None

    cleanup_notification_config(CREATE_CONFIG_ID)


def test_delete_notification_config(deleted_notification_config):
    assert snippets_notification_configs.delete_notification_config(
        ORG_ID, DELETE_CONFIG_ID
    )


def test_get_notification_config(new_notification_config_for_get):
    retrieved_config = snippets_notification_configs.get_notification_config(
        ORG_ID, GET_CONFIG_ID
    )
    assert retrieved_config is not None


def test_list_notification_configs():
    iterator = snippets_notification_configs.list_notification_configs(ORG_ID)
    assert iterator is not None


def test_update_notification_config(new_notification_config_for_update):
    updated_config = snippets_notification_configs.update_notification_config(
        ORG_ID, UPDATE_CONFIG_ID, PUBSUB_TOPIC
    )
    assert updated_config is not None


def test_receive_notifications():
    assert snippets_notification_receiver.receive_notifications(
        PROJECT_ID, PUBSUB_SUBSCRIPTION
    )
