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


# Deleting user event using Retail API.
#
import google.auth
from google.cloud.retail import PurgeUserEventsRequest, UserEventServiceClient

from setup_events.setup_cleanup import write_user_event

project_id = google.auth.default()[1]

default_catalog = f"projects/{project_id}/locations/global/catalogs/default_catalog"

visitor_id = "test_visitor_id"


# get purge user event request
def get_purge_user_event_request():
    purge_user_event_request = PurgeUserEventsRequest()
    # TO CHECK ERROR HANDLING SET INVALID FILTER HERE:
    purge_user_event_request.filter = f'visitorId="{visitor_id}"'
    purge_user_event_request.parent = default_catalog
    purge_user_event_request.force = True
    print("---purge user events request---")
    print(purge_user_event_request)
    return purge_user_event_request


# call the Retail API to purge user event
def call_purge_user_events():
    purge_operation = UserEventServiceClient().purge_user_events(
        get_purge_user_event_request()
    )

    print("---the purge operation was started:----")
    print(purge_operation.operation.name)


write_user_event(visitor_id)
call_purge_user_events()
