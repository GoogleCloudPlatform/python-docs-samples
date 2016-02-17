# Copyright 2015, Google, Inc.
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

from gcloud import datastore
from testing import CloudTest, mark_flaky

from . import tasks


@mark_flaky
class DatastoreTasksTest(CloudTest):

    def setUp(self):
        super(DatastoreTasksTest, self).setUp()
        self.client = datastore.Client(self.config.GCLOUD_PROJECT)

    def tearDown(self):
        super(DatastoreTasksTest, self).tearDown()
        with self.client.batch():
            self.client.delete_multi(
                [x.key for x in self.client.query(kind='Task').fetch()])

    def test_create_client(self):
        tasks.create_client(self.config.GCLOUD_PROJECT)

    def test_add_task(self):
        task_key = tasks.add_task(self.client, 'Test task')
        task = self.client.get(task_key)
        self.assertTrue(task)
        self.assertEqual(task['description'], 'Test task')

    def test_mark_done(self):
        task_key = tasks.add_task(self.client, 'Test task')
        tasks.mark_done(self.client, task_key.id)
        task = self.client.get(task_key)
        self.assertTrue(task)
        self.assertTrue(task['done'])

    def test_list_tasks(self):
        task1_key = tasks.add_task(self.client, 'Test task 1')
        task2_key = tasks.add_task(self.client, 'Test task 2')
        task_list = tasks.list_tasks(self.client)
        self.assertEqual([x.key for x in task_list], [task1_key, task2_key])

    def test_delete_task(self):
        task_key = tasks.add_task(self.client, 'Test task 1')
        tasks.delete_task(self.client, task_key.id)
        self.assertIsNone(self.client.get(task_key))

    def test_format_tasks(self):
        task1_key = tasks.add_task(self.client, 'Test task 1')
        tasks.add_task(self.client, 'Test task 2')
        tasks.mark_done(self.client, task1_key.id)

        output = tasks.format_tasks(tasks.list_tasks(self.client))

        self.assertTrue('Test task 1' in output)
        self.assertTrue('Test task 2' in output)
        self.assertTrue('done' in output)
        self.assertTrue('created' in output)
