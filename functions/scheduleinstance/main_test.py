# Copyright 2018, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import json
from mock import MagicMock
import pytest

import main

TEST_PROJECT = 'test-project'
TEST_ZONE = 'test-zone'
TEST_INSTANCE = 'test-instance'


@pytest.fixture(scope="session", autouse=True)
def instance():
    main._compute = MagicMock()


def test_start_instance_pubsub():
    data = base64.b64encode(json.dumps({
        'project': TEST_PROJECT,
        'zone': TEST_ZONE,
        'instance': TEST_INSTANCE
    }).encode('utf-8'))
    event = {
        'data': data
    }

    main.start_instance_pubsub(event, None)
    assert True


def test_start_instance_pubsub_fails_missing_project():
    data = base64.b64encode(json.dumps({
        'zone': TEST_ZONE,
        'instance': TEST_INSTANCE
    }).encode('utf-8'))
    event = {
        'data': data
    }

    with pytest.raises(ValueError):
        main.start_instance_pubsub(event, None)


def test_start_instance_pubsub_fails_missing_zone():
    data = base64.b64encode(json.dumps({
        'project': TEST_PROJECT,
        'instance': TEST_INSTANCE
    }).encode('utf-8'))
    event = {
        'data': data
    }

    with pytest.raises(ValueError):
        main.start_instance_pubsub(event, None)


def test_start_instance_pubsub_fails_missing_instance():
    data = base64.b64encode(json.dumps({
        'project': TEST_PROJECT,
        'zone': TEST_ZONE
    }).encode('utf-8'))
    event = {
        'data': data
    }

    with pytest.raises(ValueError):
        main.start_instance_pubsub(event, None)


def test_start_instance_pubsub_fails_missing_data():
    event = {}

    with pytest.raises(ValueError):
        main.start_instance_pubsub(event, None)


def test_stop_instance_pubsub():
    data = base64.b64encode(json.dumps({
        'project': TEST_PROJECT,
        'zone': TEST_ZONE,
        'instance': TEST_INSTANCE
    }).encode('utf-8'))
    event = {
        'data': data
    }

    main.stop_instance_pubsub(event, None)
    assert True


def test_stop_instance_pubsub_fails_missing_project():
    data = base64.b64encode(json.dumps({
        'zone': TEST_ZONE,
        'instance': TEST_INSTANCE
    }).encode('utf-8'))
    event = {
        'data': data
    }

    with pytest.raises(ValueError):
        main.stop_instance_pubsub(event, None)


def test_stop_instance_pubsub_fails_missing_zone():
    data = base64.b64encode(json.dumps({
        'project': TEST_PROJECT,
        'instance': TEST_INSTANCE
    }).encode('utf-8'))
    event = {
        'data': data
    }

    with pytest.raises(ValueError):
        main.stop_instance_pubsub(event, None)


def test_stop_instance_pubsub_fails_missing_instance():
    data = base64.b64encode(json.dumps({
        'project': TEST_PROJECT,
        'zone': TEST_ZONE
    }).encode('utf-8'))
    event = {
        'data': data
    }

    with pytest.raises(ValueError):
        main.stop_instance_pubsub(event, None)


def test_stop_instance_pubsub_fails_missing_data():
    event = {}

    with pytest.raises(ValueError):
        main.stop_instance_pubsub(event, None)
