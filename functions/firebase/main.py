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

# [START functions_firebase_rtdb]
# [START functions_firebase_firestore]
# [START functions_firebase_auth]
import json
# [END functions_firebase_rtdb]
# [END functions_firebase_firestore]
# [END functions_firebase_auth]


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
