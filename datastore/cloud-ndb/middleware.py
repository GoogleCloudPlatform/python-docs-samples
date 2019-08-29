# Copyright 2019 Google LLC All Rights Reserved.
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

# [START ndb_wsgi_middleware]
# [START ndb_django_middleware]
from google.cloud import ndb


# [END ndb_django_middleware]
def ndb_wsgi_middleware(wsgi_app):
    client = ndb.Client()

    def middleware(environ, start_response):
        with client.context():
            return wsgi_app(environ, start_response)

    return middleware
# [END ndb_wsgi_middleware]


# [START ndb_django_middleware]
def ndb_django_middleware(get_response):
    client = ndb.Client()

    def middleware(request):
        with client.context():
            return get_response(request)

    return middleware
# [END ndb_django_middleware]
