#!/usr/bin/env python
#
# Copyright 2024 Google LLC
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

import backoff
from google.api_core.exceptions import InternalServerError, NotFound, ServiceUnavailable

import snippets_notification_configs_v2

ORG_ID = os.environ["GCLOUD_ORGANIZATION"]
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
PUBSUB_TOPIC = os.environ["GCLOUD_PUBSUB_TOPIC"]
PUBSUB_SUBSCRIPTION = os.environ["GCLOUD_PUBSUB_SUBSCRIPTION"]
LOCATION_ID = os.environ["GCLOUD_LOCATION"]

CREATE_CONFIG_ID = "new-notification-pytest" + str(uuid.uuid1())


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_create_notification_config():
    # create_config_id = "new-notification-pytest" + str(uuid.uuid1())
    created_notification_config = (
        snippets_notification_configs_v2.create_notification_config(
            f"organizations/{ORG_ID}", LOCATION_ID, PUBSUB_TOPIC, CREATE_CONFIG_ID
        )
    )
    assert created_notification_config is not None
    assert CREATE_CONFIG_ID in created_notification_config.name


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_get_notification_config():
    retrieved_config = snippets_notification_configs_v2.get_notification_config(
        f"organizations/{ORG_ID}", LOCATION_ID, CREATE_CONFIG_ID
    )
    assert retrieved_config is not None


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_list_notification_configs():
    iterator = snippets_notification_configs_v2.list_notification_configs(
        f"organizations/{ORG_ID}", LOCATION_ID
    )
    assert iterator is not None
    names = []
    for item in iterator:
        names.append(item.name)
    assert any(CREATE_CONFIG_ID in name for name in names), "not found"


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_update_notification_config():
    updated_config = snippets_notification_configs_v2.update_notification_config(
        f"organizations/{ORG_ID}", LOCATION_ID, PUBSUB_TOPIC, CREATE_CONFIG_ID
    )
    assert updated_config is not None
    assert CREATE_CONFIG_ID in updated_config.name


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_receive_notifications():
    assert snippets_notification_configs_v2.receive_notifications(PUBSUB_SUBSCRIPTION)


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_delete_notification_config():
    snippets_notification_configs_v2.delete_notification_config(
        f"organizations/{ORG_ID}", LOCATION_ID, CREATE_CONFIG_ID
    )
    iterator = snippets_notification_configs_v2.list_notification_configs(
        f"organizations/{ORG_ID}", LOCATION_ID
    )
    names = []
    for item in iterator:
        names.append(item.name)
    assert CREATE_CONFIG_ID not in names
