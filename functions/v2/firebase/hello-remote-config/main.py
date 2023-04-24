# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START functions_cloudevent_firebase_remote_config]
from cloudevents.http import CloudEvent
import functions_framework


@functions_framework.cloud_event
def hello_remote_config(event: CloudEvent) -> None:
    """Triggered by a change to a Firebase Remote Config value.
    Args:
        event: Cloud Event triggered by change to Firebase Remote Config
    """
    print(f'Update type: {event.data["updateType"]}')
    print(f'Origin: {event.data["updateOrigin"]}')
    print(f'Version: {event.data["versionNumber"]}')


# [END functions_cloudevent_firebase_remote_config]
