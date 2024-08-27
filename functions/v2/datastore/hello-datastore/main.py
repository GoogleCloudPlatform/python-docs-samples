# Copyright 2024 Google LLC
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

# [START functions_cloudevent_datastore]
from cloudevents.http import CloudEvent
import functions_framework
from google.events.cloud import datastore


@functions_framework.cloud_event
def hello_datastore(cloud_event: CloudEvent) -> None:
    """Triggers by a change to a Firestore entity.

    Args:
        cloud_event: cloud event with information on the firestore event trigger
    """
    datastore_payload = datastore.EntityEventData()
    datastore_payload._pb.ParseFromString(cloud_event.data)

    print(f"Function triggered by change to: {cloud_event['source']}")

    print("\nOld value:")
    print(datastore_payload.old_value)

    print("\nNew value:")
    print(datastore_payload.value)


# [END functions_cloudevent_datastore]
