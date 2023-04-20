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


# Starts a user event rejoin operation using Retail API.
#
import google.auth
from google.cloud.retail import RejoinUserEventsRequest, UserEventServiceClient

from setup_events.setup_cleanup import purge_user_event, write_user_event

project_id = google.auth.default()[1]

default_catalog = f"projects/{project_id}/locations/global/catalogs/default_catalog"

visitor_id = "test_visitor_id"


# get rejoin user event request
def get_rejoin_user_event_request():
    # TO CHECK THE ERROR HANDLING TRY TO PASS INVALID CATALOG:
    # default_catalog = f"projects/{project_id}/locations/global/catalogs/invalid_catalog"
    rejoin_user_event_request = RejoinUserEventsRequest()
    rejoin_user_event_request.parent = default_catalog
    rejoin_user_event_request.user_event_rejoin_scope = (
        RejoinUserEventsRequest.UserEventRejoinScope.UNJOINED_EVENTS
    )
    print("---rejoin user events request---")
    print(rejoin_user_event_request)
    return rejoin_user_event_request


# call the Retail API to rejoin user event
def call_rejoin_user_events():
    rejoin_operation = UserEventServiceClient().rejoin_user_events(
        get_rejoin_user_event_request()
    )

    print("---the rejoin operation was started:----")
    print(rejoin_operation.operation.name)


write_user_event(visitor_id)
call_rejoin_user_events()
purge_user_event(visitor_id)
