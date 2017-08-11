# Copyright 2016 Google Inc. All Rights Reserved.
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

import mock

import app_engine_queue_snippets

TEST_PROJECT_ID = 'mock-project'
TEST_LOCATION = 'us-central1'
API_KEY = 'mock-api-key'
TEST_QUEUE_NAME = 'projects/{}/locations/{}/queues/{}'.format(
    TEST_PROJECT_ID, TEST_LOCATION, 'my-push-queue')


@mock.patch('app_engine_queue_snippets.get_client')
def test_list_queues(get_client):
    locations = get_client.return_value.projects.return_value.locations
    queues = locations.return_value.queues
    execute_function = queues.return_value.list.return_value.execute
    execute_function.return_value = {'name': 'task_name', 'queues': []}
    app_engine_queue_snippets.list_queues(API_KEY, TEST_PROJECT_ID,
                                          TEST_LOCATION)
    assert execute_function.called


@mock.patch('app_engine_queue_snippets.get_client')
def test_create_task(get_client):
    projects = get_client.return_value.projects.return_value
    locations = projects.locations.return_value
    create_function = locations.queues.return_value.tasks.return_value.create
    execute_function = create_function.return_value.execute
    execute_function.return_value = {'name': 'task_name'}
    app_engine_queue_snippets.create_task(API_KEY, TEST_QUEUE_NAME)
    assert execute_function.called

