# Copyright 2018 Google LLC
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

# [START functions_firebase_analytics]
from datetime import datetime
# [END functions_firebase_analytics]

# [START functions_firebase_rtdb]
# [START functions_firebase_firestore]
# [START functions_firebase_auth]
import json
# [END functions_firebase_rtdb]
# [END functions_firebase_firestore]
# [END functions_firebase_auth]

# [START functions_firebase_reactive]
from google.cloud import firestore
# [END functions_firebase_reactive]


# [START functions_firebase_rtdb]
def hello_rtdb(data, context):
    """ Triggered by a change to a Firebase RTDB reference.
    Args:
        data (dict): The event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    trigger_resource = context.resource

    print('Function triggered by change to: %s' % trigger_resource)
    print('Admin?: %s' % data.get("admin", False))
    print('Delta:')
    print(json.dumps(data["delta"]))
# [END functions_firebase_rtdb]


# [START functions_firebase_firestore]
def hello_firestore(data, context):
    """ Triggered by a change to a Firestore document.
    Args:
        data (dict): The event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    trigger_resource = context.resource

    print('Function triggered by change to: %s' % trigger_resource)

    print('\nOld value:')
    print(json.dumps(data["oldValue"]))

    print('\nNew value:')
    print(json.dumps(data["value"]))
# [END functions_firebase_firestore]


# [START functions_firebase_auth]
def hello_auth(data, context):
    """ Triggered by creation or deletion of a Firebase Auth user object.
     Args:
            data (dict): The event payload.
            context (google.cloud.functions.Context): Metadata for the event.
    """
    print('Function triggered by creation/deletion of user: %s' % data["uid"])
    print('Created at: %s' % data["metadata"]["createdAt"])

    if 'email' in data:
        print('Email: %s' % data["email"])
# [END functions_firebase_auth]


# [START functions_firebase_reactive]
client = firestore.Client()


# Converts strings added to /messages/{pushId}/original to uppercase
def make_upper_case(data, context):
    path_parts = context.resource.split('/documents/')[1].split('/')
    collection_path = path_parts[0]
    document_path = '/'.join(path_parts[1:])

    affected_doc = client.collection(collection_path).document(document_path)

    cur_value = data["value"]["fields"]["original"]["stringValue"]
    new_value = cur_value.upper()

    if cur_value != new_value:
        print(f'Replacing value: {cur_value} --> {new_value}')
        affected_doc.set({
            'original': new_value
        })
    else:
        # Value is already upper-case
        # Don't perform a second write (which can trigger an infinite loop)
        print('Value is already upper-case.')
# [END functions_firebase_reactive]


# [START functions_firebase_analytics]
def hello_analytics(data, context):
    """ Triggered by a Google Analytics for Firebase log event.
     Args:
            data (dict): The event payload.
            context (google.cloud.functions.Context): Metadata for the event.
    """
    trigger_resource = context.resource
    print(f'Function triggered by the following event: {trigger_resource}')

    event = data["eventDim"][0]
    print(f'Name: {event["name"]}')

    event_timestamp = int(event["timestampMicros"][:-6])
    print(f'Timestamp: {datetime.utcfromtimestamp(event_timestamp)}')

    user_obj = data["userDim"]
    print(f'Device Model: {user_obj["deviceInfo"]["deviceModel"]}')

    geo_info = user_obj["geoInfo"]
    print(f'Location: {geo_info["city"]}, {geo_info["country"]}')
# [END functions_firebase_analytics]


# [START functions_firebase_remote_config]
def hello_remote_config(data, context):
    """ Triggered by a change to a Firebase Remote Config value.
     Args:
            data (dict): The event payload.
            context (google.cloud.functions.Context): Metadata for the event.
    """
    print(f'Update type: {data["updateType"]}')
    print(f'Origin: {data["updateOrigin"]}')
    print(f'Version: {data["versionNumber"]}')
# [END functions_firebase_remote_config]
