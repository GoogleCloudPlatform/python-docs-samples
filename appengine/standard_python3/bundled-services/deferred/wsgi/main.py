# Copyright 2022 Google LLC
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

# [START gae_deferred_handler_wsgi]
import os
import re

from google.appengine.api import wrap_wsgi_app
from google.appengine.ext import deferred
from google.appengine.ext import ndb

my_key = os.environ.get("GAE_VERSION", "Missing")


class Counter(ndb.Model):
    count = ndb.IntegerProperty(indexed=False)


def do_something_later(key, amount):
    entity = Counter.get_or_insert(key, count=0)
    entity.count += amount
    entity.put()


def IncrementCounter(environ, start_response):
    # Use default URL and queue name, no task name, execute ASAP.
    deferred.defer(do_something_later, my_key, 10)

    # Use default URL and queue name, no task name, execute after 10s.
    deferred.defer(do_something_later, my_key, 10, _countdown=20)

    # Providing non-default task queue arguments
    deferred.defer(do_something_later, my_key, 10, _url="/custom/path", _countdown=40)

    start_response("200 OK", [("Content-Type", "text/html")])
    return ["Deferred counter increment.".encode("utf-8")]


def ViewCounter(environ, start_response):
    counter = Counter.get_or_insert(my_key, count=0)
    start_response("200 OK", [("Content-Type", "text/html")])
    return [str(counter.count).encode("utf-8")]


class CustomDeferredHandler(deferred.Handler):
    """Deferred task handler that adds additional logic."""

    def post(self, environ):
        print("Executing deferred task.")
        return super().post(environ)


routes = {
    "counter/increment": IncrementCounter,
    "counter/get": ViewCounter,
    "custom/path": CustomDeferredHandler(),
}


class WSGIApplication:
    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "").lstrip("/")
        for regex, handler in routes.items():
            match = re.search(regex, path)
            if match is not None:
                return handler(environ, start_response)

        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return ["Not found".encode("utf-8")]


app = wrap_wsgi_app(WSGIApplication(), use_deferred=True)
# [END gae_deferred_handler_wsgi]
