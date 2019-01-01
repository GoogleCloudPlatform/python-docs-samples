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

# [START all]
"""A simple counter with App Engine pull queue."""

import logging
import os
import time

from google.appengine.api import taskqueue
from google.appengine.ext import ndb
from google.appengine.runtime import apiproxy_errors
import jinja2
import webapp2


JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class Counter(ndb.Model):
    count = ndb.IntegerProperty(indexed=False)


class CounterHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {'counters': Counter.query()}
        counter_template = JINJA_ENV.get_template('counter.html')
        self.response.out.write(counter_template.render(template_values))

    # [START adding_task]
    def post(self):
        key = self.request.get('key')
        if key:
            queue = taskqueue.Queue('pullq')
            queue.add(taskqueue.Task(payload='', method='PULL', tag=key))
        self.redirect('/')
    # [END adding_task]


@ndb.transactional
def update_counter(key, tasks):
    counter = Counter.get_or_insert(key, count=0)
    counter.count += len(tasks)
    counter.put()


class CounterWorker(webapp2.RequestHandler):
    def get(self):
        """Indefinitely fetch tasks and update the datastore."""
        queue = taskqueue.Queue('pullq')
        while True:
            try:
                tasks = queue.lease_tasks_by_tag(3600, 1000, deadline=60)
            except (taskqueue.TransientError,
                    apiproxy_errors.DeadlineExceededError) as e:
                logging.exception(e)
                time.sleep(1)
                continue

            if tasks:
                key = tasks[0].tag

                try:
                    update_counter(key, tasks)
                except Exception as e:
                    logging.exception(e)
                    raise
                finally:
                    queue.delete_tasks(tasks)

            time.sleep(1)


app = webapp2.WSGIApplication([
    ('/', CounterHandler),
    ('/_ah/start', CounterWorker)
], debug=True)
# [END all]
