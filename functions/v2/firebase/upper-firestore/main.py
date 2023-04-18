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

# [START functions_cloudevent_firebase_reactive]
from cloudevents.http import CloudEvent
import functions_framework
from google.cloud import firestore
from google.events.cloud import firestore as firestoredata

client = firestore.Client()


# Converts strings added to /messages/{pushId}/original to uppercase
@functions_framework.cloud_event
def make_upper_case(cloud_event: CloudEvent) -> None:
    firestore_payload = firestoredata.DocumentEventData()
    firestore_payload._pb.ParseFromString(cloud_event.data)

    path_parts = firestore_payload.value.name.split("/")
    separator_idx = path_parts.index("documents")
    collection_path = path_parts[separator_idx + 1]
    document_path = "/".join(path_parts[(separator_idx + 2) :])

    print(f"Collection path: {collection_path}")
    print(f"Document path: {document_path}")

    affected_doc = client.collection(collection_path).document(document_path)

    cur_value = firestore_payload.value.fields["original"].string_value
    new_value = cur_value.upper()

    if cur_value != new_value:
        print(f"Replacing value: {cur_value} --> {new_value}")
        affected_doc.set({"original": new_value})
    else:
        # Value is already upper-case
        # Don't perform a second write (which can trigger an infinite loop)
        print("Value is already upper-case.")


# [END functions_cloudevent_firebase_reactive]
