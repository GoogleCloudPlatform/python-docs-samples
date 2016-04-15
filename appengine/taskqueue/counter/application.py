# Copyright 2016 Google Inc. All rights reserved.
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

from google.appengine.api import taskqueue
from google.appengine.ext import ndb
import webapp2


COUNTER_KEY = 'default counter'


class Counter(ndb.Model):
    count = ndb.IntegerProperty(indexed=False)


class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        counter = Counter.get_by_id(COUNTER_KEY)
        count = counter.count if counter else 0

        self.response.write("""
            Count: {count}<br>
            <form method="post" action="/enqueue">
                <label>Increment amount</label>
                <input name="amount" value="1">
                <button>Enqueue task</button>
            </form>
        """.format(count=count))


class EnqueueTaskHandler(webapp2.RequestHandler):
    def post(self):
        amount = int(self.request.get('amount'))

        task = taskqueue.add(
            url='/update_counter',
            target='worker',
            params={'amount': amount})

        self.response.write(
            'Task {} enqueued, ETA {}.'.format(task.name, task.eta))


class AsyncEnqueueTaskHandler(webapp2.RequestHandler):
    def post(self):
        amount = int(self.request.get('amount'))

        future = taskqueue.add_async(
            url='/update_counter',
            target='worker',
            params={'amount': amount})

        task = future.wait()

        self.response.write(
            'Task {} enqueued, ETA {}.'.format(task.name, task.eta))


app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
    ('/enqueue', EnqueueTaskHandler),
    ('/enqueue_async', EnqueueTaskHandler)
], debug=True)
