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

import create_app_engine_queue_task

TEST_PROJECT = 'mock-project'
TEST_LOCATION = 'us-central1'
TEST_QUEUE = 'my-appengine-queue'


@mock.patch('googleapiclient.discovery.build')
def test_create_task(build):
    projects = build.return_value.projects.return_value
    locations = projects.locations.return_value
    create_function = locations.queues.return_value.tasks.return_value.create
    execute_function = create_function.return_value.execute
    execute_function.return_value = {'name': 'task_name'}
    create_app_engine_queue_task.create_task(
        TEST_PROJECT, TEST_QUEUE, TEST_LOCATION)
    assert execute_function.called
