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

import os
import pytest
import uuid


os.environ['LOCATION'] = 'us-central1'
os.environ['QUEUE'] = str(uuid.uuid4())

# Cannot import main until some environment variables have been set up
import main     # noqa: E402


TEST_NAME = 'taskqueue-migration-' + os.environ['QUEUE']
TEST_TASKS = {
    'alpha': 2,
    'beta': 1,
    'gamma': 3
}


@pytest.fixture(scope='module')
def queue():
    # Setup - create unique Cloud Tasks queue
    project = main.project
    location = main.location
    parent = 'projects/{}/locations/{}'.format(project, location)

    queue = main.client.create_queue(
        parent=parent,
        queue={'name': parent + '/queues/' + TEST_NAME}
    )

    yield queue

    # Teardown - delete test queue, which also deletes tasks

    main.client.delete_queue(name='{}/queues/{}'.format(parent, TEST_NAME))


@pytest.fixture(scope='module')
def entity_kind():
    yield TEST_NAME

    # Teardown - Delete test entities
    datastore_client = main.datastore_client
    query = datastore_client.query(kind=TEST_NAME)
    keys = [entity.key for entity in query.fetch()]
    datastore_client.delete_multi(keys)


def test_get_home_page(queue, entity_kind):
    # Set main globals to test values
    save_queue = main.queue_name
    save_entity_kind = main.entity_kind
    main.queue = queue.name
    main.entity_kind = entity_kind

    main.app.testing = True
    client = main.app.test_client()

    # Counter list should be empty
    r = client.get('/')
    assert r.status_code == 200
    assert 'Counters' in r.data.decode('utf-8')
    assert '<li>' not in r.data.decode('utf-8')     # List is empty

    # Restore main globals
    main.queue_name = save_queue
    main.entity_kind = save_entity_kind


def test_enqueuetasks(queue):
    # Set main globals to test values
    save_queue = main.queue
    main.queue = queue.name

    main.app.testing = True
    client = main.app.test_client()

    # Post tasks stage, queueing them up
    for task in TEST_TASKS:
        for i in range(TEST_TASKS[task]):
            r = client.post('/', data={'key': task})
            assert r.status_code == 302
            assert r.headers.get('location').count('/') == 3

    # See if tasks have been created
    counters_found = {}
    tasks = main.client.list_tasks(parent=queue.name)
    for task in tasks:
        details = main.client.get_task(
            request={
                'name': task.name,
                'response_view': main.tasks.Task.View.FULL
            }
        )

        key = details.app_engine_http_request.body.decode()
        if key not in counters_found:
            counters_found[key] = 0
        counters_found[key] += 1

    # Did every POST result in a task?
    for key in TEST_TASKS:
        assert key in counters_found
        assert TEST_TASKS[key] == counters_found[key]

    # Did every task come from a POST?
    for key in counters_found:
        assert key in TEST_TASKS
        assert counters_found[key] == TEST_TASKS[key]

    # Restore main globals
    main.queue = save_queue


def test_processtasks(entity_kind):
    # Set main globals to test values
    save_entity_kind = main.entity_kind
    main.entity_kind = entity_kind

    main.app.testing = True
    client = main.app.test_client()

    # Push tasks as if from Cloud Tasks
    for key in TEST_TASKS:
        for i in range(TEST_TASKS[key]):
            r = client.post(
                '/push-task',
                data=key,
                content_type='text/plain',
                headers=[('X-AppEngine-QueueName', main.queue_name)]
            )

        assert r.status_code == 200
        assert r.data == b'OK'

    # Push tasks with bad X-AppEngine-QueueName header
    r = client.post(
            '/push-task',
            data=key,
            content_type='text/plain',
            headers=[('X-AppEngine-QueueName', 'WRONG-NAME')]
        )
    assert r.status_code == 200
    assert r.data == b'REJECTED'

    r = client.post(
            '/push-task',
            data=key,
            content_type='text/plain'
        )
    assert r.status_code == 200
    assert r.data == b'REJECTED'

    # See that all the tasks were correctly processed
    r = client.get('/')
    assert r.status_code == 200
    assert 'Counters' in r.data.decode('utf-8')
    for key in TEST_TASKS:
        assert '{}: {}'.format(key, TEST_TASKS[key]) in r.data.decode('utf-8')

    # Restore main globals
    main.entity_kind = save_entity_kind
