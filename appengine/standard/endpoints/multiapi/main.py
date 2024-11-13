# Copyright 2016 Google Inc.
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

"""This is a sample multi-class API implemented using Cloud Ednpoints"""

import endpoints
from protorpc import messages
from protorpc import remote


class Request(messages.Message):
    message = messages.StringField(1)


class Response(messages.Message):
    message = messages.StringField(1)


# [START endpoints_multiclass]
api_collection = endpoints.api(name="library", version="v1.0")


@api_collection.api_class(resource_name="shelves")
class Shelves(remote.Service):
    @endpoints.method(Request, Response)
    def list(self, request):
        return Response()


# [START endpoints_books]
@api_collection.api_class(resource_name="books", path="books")
class Books(remote.Service):
    @endpoints.method(Request, Response, path="bookmark")
    def get_bookmark(self, request):
        return Response()

    @endpoints.method(Request, Response)
    def best_sellers_list(self, request):
        return Response()


# [END endpoints_books]
# [END endpoints_multiclass]


# [START endpoints_api_server]
api = endpoints.api_server([api_collection])
# [END endpoints_api_server]
