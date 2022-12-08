# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Write user event using Retail API.
#
import datetime

import google.auth
from google.cloud.retail import UserEvent, UserEventServiceClient, WriteUserEventRequest
from google.protobuf.timestamp_pb2 import Timestamp

from setup_events.setup_cleanup import purge_user_event

project_id = google.auth.default()[1]

default_catalog = f"projects/{project_id}/locations/global/catalogs/default_catalog"

visitor_id = "test_visitor_id"


# get user event
def get_user_event():
    timestamp = Timestamp()
    timestamp.seconds = int(datetime.datetime.now().timestamp())

    user_event = UserEvent()
    user_event.event_type = "home-page-view"
    user_event.visitor_id = visitor_id
    user_event.event_time = timestamp

    print(user_event)
    return user_event


# get write user event request
def get_write_event_request(user_event):
    # TO CHECK THE ERROR HANDLING TRY TO PASS INVALID CATALOG:
    # default_catalog = f"projects/{project_id}/locations/global/catalogs/invalid_catalog"
    write_user_event_request = WriteUserEventRequest()
    write_user_event_request.user_event = user_event
    write_user_event_request.parent = default_catalog

    print("---write user event request---")
    print(write_user_event_request)

    return write_user_event_request


# call the Retail API to write user event
def write_user_event():
    write_user_event_request = get_write_event_request(get_user_event())
    user_event = UserEventServiceClient().write_user_event(write_user_event_request)

    print("---written user event:---")
    print(user_event)
    return user_event


write_user_event()
purge_user_event(visitor_id)
