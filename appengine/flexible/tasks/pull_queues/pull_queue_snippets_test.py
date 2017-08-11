# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import pull_queue_snippets

TEST_PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
TEST_LOCATION = 'us-central1'
API_KEY = os.getenv('API_KEY')


def test_list_queues():
    result = pull_queue_snippets.list_queues(
        API_KEY, TEST_PROJECT_ID, TEST_LOCATION)
    assert len(result['queues']) > 0


def test_create_task():
    result = pull_queue_snippets.list_queues(
        API_KEY, TEST_PROJECT_ID, TEST_LOCATION)
    queue_name = result['queues'][0]['name']
    result = pull_queue_snippets.create_task(API_KEY, queue_name)
    assert queue_name in result['name']


def test_pull_and_ack_task():
    result = pull_queue_snippets.list_queues(
        API_KEY, TEST_PROJECT_ID, TEST_LOCATION)
    queue_name = result['queues'][0]['name']
    pull_queue_snippets.create_task(API_KEY, queue_name)
    task = pull_queue_snippets.pull_task(API_KEY, queue_name)
    pull_queue_snippets.acknowledge_task(API_KEY, task)

