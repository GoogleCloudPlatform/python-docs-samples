# Copyright 2015 Google Inc. All rights reserved.
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

"""
Sample App Engine application demonstrating how to use the Namespace Manager
API with Memcache.

For more information, see README.md.
"""

# [START all]
from google.appengine.api import namespace_manager
from google.appengine.api import taskqueue
from google.appengine.ext import ndb
import webapp2


class Counter(ndb.Model):
    count = ndb.IntegerProperty()


@ndb.transactional
def update_counter(name):
    """Increment the named counter by 1."""
    counter = Counter.get_by_id(name)
    if counter is None:
        counter = Counter(id=name, count=0)

    counter.count += 1
    counter.put()

    return counter.count


def get_count(name):
    counter = Counter.get_by_id(name)
    if not counter:
        return 0
    return counter.count


class DeferredCounterHandler(webapp2.RequestHandler):
    def post(self):
        name = self.request.get('counter_name')
        update_counter(name)


class TaskQueueCounterHandler(webapp2.RequestHandler):
    """Queues two tasks to increment a counter in global namespace as well as
    the namespace is specified by the request, which is arbitrarily named
    'default' if not specified."""
    def get(self, namespace='default'):
        # Queue task to update global counter.
        current_global_count = get_count('counter')
        taskqueue.add(
            url='/tasks/counter',
            params={'counter_name': 'counter'})

        # Queue task to update counter in specified namespace.
        previous_namespace = namespace_manager.get_namespace()
        try:
            namespace_manager.set_namespace(namespace)
            current_namespace_count = get_count('counter')
            taskqueue.add(
                url='/tasks/counter',
                params={'counter_name': 'counter'})
        finally:
            namespace_manager.set_namespace(previous_namespace)

        self.response.write(
            'Counters will be updated asyncronously.'
            'Current values: Global: {}, Namespace {}: {}'.format(
                current_global_count, namespace, current_namespace_count))


app = webapp2.WSGIApplication([
    (r'/tasks/counter', DeferredCounterHandler),
    (r'/taskqueue', TaskQueueCounterHandler),
    (r'/taskqueue/(.*)', TaskQueueCounterHandler)
], debug=True)
