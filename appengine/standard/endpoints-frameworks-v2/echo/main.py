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

"""This is a sample Hello World API implemented using Google Cloud
Endpoints."""

# [START imports]
import endpoints
from protorpc import message_types
from protorpc import messages
from protorpc import remote
# [END imports]


# [START messages]
class Echo(messages.Message):
    """A proto Message that contains a simple string field."""
    content = messages.StringField(1)
# [END messages]


# [START echo_api]
@endpoints.api(name='echo', version='v1')
class EchoApi(remote.Service):

    @endpoints.method(
        # This method takes an Echo message.
        Echo,
        # This method returns an Echo message.
        Echo,
        path='echo',
        http_method='POST',
        name='echo')
    def echo(self, request):
        return Echo(content=request.content)

    @endpoints.method(
        # This method takes an empty request body.
        message_types.VoidMessage,
        # This method returns an Echo message.
        Echo,
        path='echo/getUserEmail',
        http_method='GET',
        # Require auth tokens to have the following scopes to access this API.
        scopes=[endpoints.EMAIL_SCOPE],
        # OAuth2 audiences allowed in incoming tokens.
        audiences=['your-oauth-client-id.com'])
    def get_user_email(self, request):
        user = endpoints.get_current_user()
        # If there's no user defined, the request was unauthenticated, so we
        # raise 401 Unauthorized.
        if not user:
            raise endpoints.UnauthorizedException
        return Echo(content=user.email())
# [END echo_api]


# [START api_server]
api = endpoints.api_server([EchoApi])
# [END api_server]
