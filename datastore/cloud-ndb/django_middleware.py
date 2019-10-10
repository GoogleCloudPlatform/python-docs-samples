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

# [START ndb_django_middleware]
from google.cloud import ndb


# Once this middleware is activated in Django settings, NDB calls inside Django
# views will be executed in context, with a separate context for each request.
def ndb_django_middleware(get_response):
    client = ndb.Client()

    def middleware(request):
        with client.context():
            return get_response(request)

    return middleware
# [END ndb_django_middleware]
