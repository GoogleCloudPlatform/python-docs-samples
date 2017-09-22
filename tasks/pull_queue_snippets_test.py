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

TEST_PROJECT_ID = os.getenv('GCLOUD_PROJECT')
TEST_LOCATION = os.getenv('TEST_QUEUE_LOCATION', 'us-central1')
TEST_QUEUE_NAME = os.getenv('TEST_QUEUE_NAME', 'my-pull-queue')


def test_create_task():
    result = pull_queue_snippets.create_task(
        TEST_PROJECT_ID, TEST_QUEUE_NAME, TEST_LOCATION)
    assert TEST_QUEUE_NAME in result['name']


def test_pull_and_ack_task():
    pull_queue_snippets.create_task(
        TEST_PROJECT_ID, TEST_QUEUE_NAME, TEST_LOCATION)
    task = pull_queue_snippets.pull_task(
        TEST_PROJECT_ID, TEST_QUEUE_NAME, TEST_LOCATION)
    pull_queue_snippets.acknowledge_task(task)
