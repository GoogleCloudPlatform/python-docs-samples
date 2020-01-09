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

from google.cloud import ndb

import django_middleware


def test_ndb_django_middleware():
    def fake_get_response(request):
        # Validate that a context is live. This will throw
        # ndb.exceptions.ContextError if no context is set up.
        ndb.context.get_context()

    wrapped_function = django_middleware.ndb_django_middleware(
        fake_get_response)

    wrapped_function(None)
