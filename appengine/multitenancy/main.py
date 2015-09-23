# Copyright 2015 Google Inc. All rights reserved.
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

# [START all]
import webapp2
from google.appengine.api import namespace_manager
from google.appengine.ext import ndb

class Counter(ndb.Model):
   """Model for containing a count."""
   count = ndb.IntegerProperty()


def update_counter(name):
   """Increment the named counter by 1."""
   def _update_counter(name):
       counter = Counter.get_by_id(name)
       if counter is None:
           counter = Counter(id=name);
           counter.count = 0
       counter.count += 1
       counter.put()
   # Update counter in a transaction.
   ndb.transaction(lambda: _update_counter(name))
   counter = Counter.get_by_id(name)
   return counter.count


class SomeRequest(webapp2.RequestHandler):
   """Perform synchronous requests to update counter."""
   def get(self):
       update_counter('SomeRequest')
       # try/finally pattern to temporarily set the namespace.
       # Save the current namespace.
       namespace = namespace_manager.get_namespace()
       try:
           namespace_manager.set_namespace('-global-')
           x = update_counter('SomeRequest')
       finally:
           # Restore the saved namespace.
           namespace_manager.set_namespace(namespace)
       self.response.write('<html><body><p>Updated counters')
       self.response.write(' to %s' % x)
       self.response.write('</p></body></html>')

app = webapp2.WSGIApplication([('/', SomeRequest)], debug=True)
# [END all]
