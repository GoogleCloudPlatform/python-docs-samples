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

# [START gae_deferred_handler_django]
import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.urls import path
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


def increment_counter(request):
    # Use default URL and queue name, no task name, execute ASAP.
    deferred.defer(do_something_later, my_key, 10)

    # Use default URL and queue name, no task name, execute after 10s.
    deferred.defer(do_something_later, my_key, 10, _countdown=20)

    # Providing non-default task queue arguments
    deferred.defer(do_something_later, my_key, 10, _url="/custom/path", _countdown=40)

    return HttpResponse("Deferred counter increment.")


def view_counter(request):
    counter = Counter.get_or_insert(my_key, count=0)
    return HttpResponse(str(counter.count))


def custom_deferred(request):
    print("Executing deferred task.")
    # request.environ contains the WSGI `environ` dictionary (See PEP 0333)
    response, status, headers = deferred.Handler().post(request.environ)
    return HttpResponse(response, status=status.value)


urlpatterns = (
    path("counter/get", view_counter, name="view_counter"),
    path("counter/increment", increment_counter, name="increment_counter"),
    path("custom/path", custom_deferred, name="custom_deferred"),
)

settings.configure(
    DEBUG=True,
    SECRET_KEY="thisisthesecretkey",
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ),
    ALLOWED_HOSTS=["*"],
)

app = wrap_wsgi_app(get_wsgi_application(), use_deferred=True)
# [END gae_deferred_handler_django]
