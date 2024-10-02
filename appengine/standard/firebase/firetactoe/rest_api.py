# Copyright 2016 Google Inc.
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

try:
    from functools import lru_cache
except ImportError:
    from functools32 import lru_cache
# [START rest_writing_data]
import json

import google.auth
from google.auth.transport.requests import AuthorizedSession

_FIREBASE_SCOPES = [
    "https://www.googleapis.com/auth/firebase.database",
    "https://www.googleapis.com/auth/userinfo.email",
]


# Memoize the authorized session, to avoid fetching new access tokens
@lru_cache()
def _get_session():
    """Provides an authed requests session object."""
    creds, _ = google.auth.default(scopes=[_FIREBASE_SCOPES])
    # Use application default credentials to make the Firebase calls
    # https://firebase.google.com/docs/reference/rest/database/user-auth
    authed_session = AuthorizedSession(creds)
    return authed_session


def firebase_put(path, value=None):
    """Writes data to Firebase.

    An HTTP PUT writes an entire object at the given database path. Updates to
    fields cannot be performed without overwriting the entire object

    Args:
        path - the url to the Firebase object to write.
        value - a json string.
    """
    response, content = _get_session().put(path, body=value)
    return json.loads(content)


def firebase_patch(path, value=None):
    """Update specific children or fields

    An HTTP PATCH allows specific children or fields to be updated without
    overwriting the entire object.

    Args:
        path - the url to the Firebase object to write.
        value - a json string.
    """
    response, content = _get_session().patch(path, body=value)
    return json.loads(content)


def firebase_post(path, value=None):
    """Add an object to an existing list of data.

    An HTTP POST allows an object to be added to an existing list of data.
    A successful request will be indicated by a 200 OK HTTP status code. The
    response content will contain a new attribute "name" which is the key for
    the child added.

    Args:
        path - the url to the Firebase list to append to.
        value - a json string.
    """
    response, content = _get_session().post(path, body=value)
    return json.loads(content)


# [END rest_writing_data]


def firebase_get(path):
    """Read the data at the given path.

    An HTTP GET request allows reading of data at a particular path.
    A successful request will be indicated by a 200 OK HTTP status code.
    The response will contain the data being retrieved.

    Args:
        path - the url to the Firebase object to read.
    """
    response, content = _get_session().get(path)
    return json.loads(content)


def firebase_delete(path):
    """Removes the data at a particular path.

    An HTTP DELETE removes the data at a particular path.  A successful request
    will be indicated by a 200 OK HTTP status code with a response containing
    JSON null.

    Args:
        path - the url to the Firebase object to delete.
    """
    response, content = _get_session().delete(path)
