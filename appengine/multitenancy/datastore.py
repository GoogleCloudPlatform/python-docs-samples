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
API with Datastore.

For more information, see README.md.
"""

# [START all]
from google.appengine.api import namespace_manager
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


class DatastoreCounterHandler(webapp2.RequestHandler):
    """Increments counters in the global namespace as well as in whichever
    namespace is specified by the request, which is arbitrarily named 'default'
    if not specified."""

    def get(self, namespace='default'):
        global_count = update_counter('counter')

        # Save the current namespace.
        previous_namespace = namespace_manager.get_namespace()
        try:
            namespace_manager.set_namespace(namespace)
            namespace_count = update_counter('counter')
        finally:
            # Restore the saved namespace.
            namespace_manager.set_namespace(previous_namespace)

        self.response.write('Global: {}, Namespace {}: {}'.format(
            global_count, namespace, namespace_count))


app = webapp2.WSGIApplication([
    (r'/datastore', DatastoreCounterHandler),
    (r'/datastore/(.*)', DatastoreCounterHandler)
], debug=True)
# [END all]
