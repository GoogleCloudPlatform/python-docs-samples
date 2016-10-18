# Copyright 2016 Google Inc. All Rights Reserved.
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

"""Demonstration of the Firebase REST API in Python"""

# [START rest_writing_data]
import base64
import json
import os
import re
import time
import urllib


from flask import request
import httplib2
from oauth2client.client import GoogleCredentials


_FIREBASE_SCOPES = [
    'https://www.googleapis.com/auth/firebase.database',
    'https://www.googleapis.com/auth/userinfo.email']


def _get_http(_memo={}):
    """Provides an authed http object."""
    if 'http' not in _memo:
        # Memoize the authorized http, to avoid fetching new access tokens
        http = httplib2.Http()
        # Use application default credentials to make the Firebase calls
        # https://firebase.google.com/docs/reference/rest/database/user-auth
        creds = GoogleCredentials.get_application_default().create_scoped(
            _FIREBASE_SCOPES)
        creds.authorize(http)
        _memo['http'] = http
    return _memo['http']
    
def firebase_put(path, value=None):
    """Writes data to Firebase. Value should be a valid json object.
     Put writes an entire object at the given database path. Updates to 
     fields cannot be performed without overwriting the entire object
     """
    response, content = _get_http().request(path, method='PUT', body=value)
    if content != "null":
        return json.loads(content)
    else:
        return None

def firebase_patch(path, value=None):
    """Allows specific children or fields to be updated without overwriting
     the entire object. Value should again be a valid json object
     """
    response, content = _get_http().request(path, method='PATCH', body=value)
    if content != "null":
        return json.loads(content)
    else:
        return None

def firebase_post(path, value=None):
    """Post allows an object to be added to an existing list of data.
     Value should once again be a valid json object. A successful request 
     will be indicated by a 200 OK HTTP status code. The response will 
     contain a new attribute "name" which is the key for the child added
     """
    response, content = _get_http().request(path, method='POST', body=value)
    if content != "null":
        return json.loads(content)
    else:
        return None

# [END rest_writing_data]
# [START rest_reading_data]
def firebase_get(path):
    """Get request allows reading of data at a particular path
     A successful request will be indicated by a 200 OK HTTP status code. 
     The response will contain the data being retrieved
     """
    response, content = _get_http().request(path, method='GET')
    if content != "null":
        return json.loads(content)
    else:
        return None
# [END rest_reading_data]
# [START rest_deleting_data]

def firebase_delete(path):
    """Delete removes the data at a particular path
     A successful request will be indicated by a 200 OK HTTP status code
     with a response containing JSON null.
     """
    response, content = _get_http().request(path, method='DELETE')
    if content != "null":
        return json.loads(content)
    else:
        return None

# [END rest_deleting_data]