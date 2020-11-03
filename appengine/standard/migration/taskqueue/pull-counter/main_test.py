# Copyright 2020 Google LLC
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

import pytest
import uuid

import main


TEST_NAME = 'taskqueue-migration-' + str(uuid.uuid4())
TEST_TASKS = {
    'alpha': 2,
    'beta': 1,
    'gamma': 3
}


@pytest.fixture(scope='module')
def subscription():
    # Setup - create unique topic and subscription
    project = main.project
    topic_name = 'projects/{}/topics/{}'.format(project, TEST_NAME)
    subscription_name = 'projects/{}/subscriptions/{}'.format(project, TEST_NAME)

    publisher = main.publisher
    publisher.create_topic(name=topic_name)

    subscriber = main.subscriber
    subscription = subscriber.create_subscription(
        name=subscription_name,
        topic=topic_name
    )

    yield subscription

    # Teardown - delete test topic and subscription
    subscriber.delete_subscription(subscription=subscription_name)
    publisher.delete_topic(topic=topic_name)


@pytest.fixture(scope='module')
def entity_kind():
    yield TEST_NAME

    # Teardown - Delete test entities
    datastore_client = main.datastore_client
    query = datastore_client.query(kind=TEST_NAME)
    keys = [entity.key for entity in query.fetch()]
    datastore_client.delete_multi(keys)


def test_get_home_page(subscription, entity_kind):
    # Set main globals to test values
    save_topic = main.topic
    save_subscription = main.subscription
    save_entity_kind = main.entity_kind

    main.topic = subscription.topic
    main.subscription = subscription.name
    main.entity_kind = entity_kind

    main.app.testing = True
    client = main.app.test_client()

    r = client.get('/')
    assert r.status_code == 200
    assert 'Counters' in r.data.decode('utf-8')
    assert '<li>' not in r.data.decode('utf-8')     # List is empty

    # Restore main globals
    main.topic = save_topic
    main.subscription = save_subscription
    main.entity_kind = save_entity_kind


# Dummy loop terminator for task processing
duration = 4


def dummy_terminator():
    global duration
    duration -= 1
    return duration > 0


def test_tasks(subscription, entity_kind):
    # Set main globals to test values
    save_topic = main.topic
    save_subscription = main.subscription
    save_entity_kind = main.entity_kind

    main.topic = subscription.topic
    main.subscription = subscription.name
    main.entity_kind = entity_kind

    main.app.testing = True
    client = main.app.test_client()

    # Post tasks stage, queueing them up
    for task in TEST_TASKS:
        for i in range(TEST_TASKS[task]):
            r = client.post('/', data={'key': task})
            assert r.status_code == 302
            assert r.headers.get('location').count('/') == 3

    # Trigger /_ah/start with terminating processing_tasks()

    save_processing_tasks = main.processing_tasks
    main.processing_tasks = dummy_terminator
    r = client.get('/_ah/start')
    main.processing_tasks = save_processing_tasks

    # See if home page lists tasks having been processed
    r = client.get('/')
    assert r.status_code == 200
    page = r.data.decode('utf-8')
    for task in TEST_TASKS:
        assert task in page
        assert str(TEST_TASKS[task]) in page

    # Restore main globals
    main.topic = save_topic
    main.subscription = save_subscription
    main.entity_kind = save_entity_kind
