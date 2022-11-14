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

# [START gae_deferred_handler_flask]
import os

from flask import Flask, request
from google.appengine.api import wrap_wsgi_app
from google.appengine.ext import deferred
from google.appengine.ext import ndb

my_key = os.environ.get("GAE_VERSION", "Missing")

app = Flask(__name__)
app.wsgi_app = wrap_wsgi_app(app.wsgi_app, use_deferred=True)


class Counter(ndb.Model):
    count = ndb.IntegerProperty(indexed=False)


def do_something_later(key, amount):
    entity = Counter.get_or_insert(key, count=0)
    entity.count += amount
    entity.put()


@app.route("/counter/increment")
def increment_counter():
    # Use default URL and queue name, no task name, execute ASAP.
    deferred.defer(do_something_later, my_key, 10)

    # Use default URL and queue name, no task name, execute after 10s.
    deferred.defer(do_something_later, my_key, 10, _countdown=20)

    # Providing non-default task queue arguments
    deferred.defer(do_something_later, my_key, 10, _url="/custom/path", _countdown=40)

    return "Deferred counter increment."


@app.route("/counter/get")
def view_counter():
    counter = Counter.get_or_insert(my_key, count=0)
    return str(counter.count)


@app.route("/custom/path", methods=["POST"])
def custom_deferred():
    print("Executing deferred task.")
    # request.environ contains the WSGI `environ` dictionary (See PEP 0333)
    return deferred.Handler().post(request.environ)


# [END gae_deferred_handler_flask]
