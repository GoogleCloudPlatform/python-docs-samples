# Copyright 2015 Google Inc
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

# [START taskqueue]
import operator
import os
import unittest

from google.appengine.api import taskqueue
from google.appengine.ext import deferred
from google.appengine.ext import testbed


class TaskQueueTestCase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        # root_path must be set the the location of queue.yaml.
        # Otherwise, only the 'default' queue will be available.
        self.testbed.init_taskqueue_stub(
            root_path=os.path.join(os.path.dirname(__file__), 'resources'))
        self.taskqueue_stub = self.testbed.get_stub(
            testbed.TASKQUEUE_SERVICE_NAME)

    def tearDown(self):
        self.testbed.deactivate()

    def testTaskAddedToQueue(self):
        taskqueue.Task(name='my_task', url='/url/of/my/task/').add()
        tasks = self.taskqueue_stub.get_filtered_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].name, 'my_task')
# [END taskqueue]

    # [START filtering]
    def testFiltering(self):
        taskqueue.Task(name='task_one', url='/url/of/task/1/').add('queue-1')
        taskqueue.Task(name='task_two', url='/url/of/task/2/').add('queue-2')

        # All tasks
        tasks = self.taskqueue_stub.get_filtered_tasks()
        self.assertEqual(len(tasks), 2)

        # Filter by name
        tasks = self.taskqueue_stub.get_filtered_tasks(name='task_one')
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].name, 'task_one')

        # Filter by URL
        tasks = self.taskqueue_stub.get_filtered_tasks(url='/url/of/task/1/')
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].name, 'task_one')

        # Filter by queue
        tasks = self.taskqueue_stub.get_filtered_tasks(queue_names='queue-1')
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].name, 'task_one')

        # Multiple queues
        tasks = self.taskqueue_stub.get_filtered_tasks(
            queue_names=['queue-1', 'queue-2'])
        self.assertEqual(len(tasks), 2)
    # [END filtering]

    # [START deferred]
    def testTaskAddedByDeferred(self):
        deferred.defer(operator.add, 1, 2)

        tasks = self.taskqueue_stub.get_filtered_tasks()
        self.assertEqual(len(tasks), 1)

        result = deferred.run(tasks[0].payload)
        self.assertEqual(result, 3)
    # [END deferred]


if __name__ == '__main__':
    unittest.main()
