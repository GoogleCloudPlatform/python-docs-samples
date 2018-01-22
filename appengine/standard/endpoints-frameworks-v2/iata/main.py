# Copyright 2018 Google Inc. All rights reserved.
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

"""This is a sample Airport Information service implemented using
Google Cloud Endpoints Frameworks for Python."""

# [START imports]
import endpoints
from protorpc import message_types
from protorpc import messages
from protorpc import remote

from data import AIRPORTS
# [END imports]

# [START messages]
IATA_RESOURCE = endpoints.ResourceContainer(
    iata=messages.StringField(1, required=True)
)


class Airport(messages.Message):
    iata = messages.StringField(1, required=True)
    name = messages.StringField(2, required=True)


IATA_AIRPORT_RESOURCE = endpoints.ResourceContainer(
    Airport,
    iata=messages.StringField(1, required=True)
)


class AirportList(messages.Message):
    airports = messages.MessageField(Airport, 1, repeated=True)
# [END messages]


# [START iata_api]
@endpoints.api(name='iata', version='v1')
class IataApi(remote.Service):
    @endpoints.method(
        IATA_RESOURCE,
        Airport,
        path='airport/{iata}',
        http_method='GET',
        name='get_airport')
    def get_airport(self, request):
        if request.iata not in AIRPORTS:
            raise endpoints.NotFoundException()
        return Airport(iata=request.iata, name=AIRPORTS[request.iata])

    @endpoints.method(
        message_types.VoidMessage,
        AirportList,
        path='airports',
        http_method='GET',
        name='list_airports')
    def list_airports(self, request):
        codes = AIRPORTS.keys()
        codes.sort()
        return AirportList(airports=[
          Airport(iata=iata, name=AIRPORTS[iata]) for iata in codes
        ])

    @endpoints.method(
        IATA_RESOURCE,
        message_types.VoidMessage,
        path='airport/{iata}',
        http_method='DELETE',
        name='delete_airport',
        api_key_required=True)
    def delete_airport(self, request):
        if request.iata not in AIRPORTS:
            raise endpoints.NotFoundException()
        del AIRPORTS[request.iata]
        return message_types.VoidMessage()

    @endpoints.method(
        Airport,
        Airport,
        path='airport',
        http_method='POST',
        name='create_airport',
        api_key_required=True)
    def create_airport(self, request):
        if request.iata in AIRPORTS:
            raise endpoints.BadRequestException()
        AIRPORTS[request.iata] = request.name
        return Airport(iata=request.iata, name=AIRPORTS[request.iata])

    @endpoints.method(
        IATA_AIRPORT_RESOURCE,
        Airport,
        path='airport/{iata}',
        http_method='POST',
        name='update_airport',
        api_key_required=True)
    def update_airport(self, request):
        if request.iata not in AIRPORTS:
            raise endpoints.BadRequestException()
        AIRPORTS[request.iata] = request.name
        return Airport(iata=request.iata, name=AIRPORTS[request.iata])
# [END iata_api]


# [START api_server]
api = endpoints.api_server([IataApi])
# [END api_server]
