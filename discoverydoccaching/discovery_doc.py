# Copyright 2015, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
A module that takes care of caching and updating discovery docs for
google-api-python-clients (until such a feature is integrated).
"""

import json
import os
import time

import httplib2

# [START build_and_update]

RESOURCE_PATH = '..'  # look for discovery docs in the parent folder
MAX_AGE = 86400  # update discovery docs older than a day

def build_and_update(api, version, scopes=None):
    from oauth2client.client import GoogleCredentials
    from googleapiclient.discovery import build_from_document

    path = os.path.join(RESOURCE_PATH, '{}.{}'.format(api, version))
    try:
        age = time.time() - os.path.getmtime(path)
        if age > MAX_AGE:
            _update_discovery_doc(api, version, path)
    except os.error:
        _update_discovery_doc(api, version, path)

    credentials = GoogleCredentials.get_application_default()
    if not scopes is None and credentials.create_scoped_required():
        credentials = credentials.create_scoped(scopes)
    with open(path, 'r') as discovery_doc:
        return build_from_document(discovery_doc.read(),
                                   http=httplib2.Http(),
                                   credentials=credentials)


def _update_discovery_doc(api, version, path):
    from apiclient.discovery import DISCOVERY_URI
    from apiclient.errors import HttpError
    from apiclient.errors import InvalidJsonError
    import uritemplate

    requested_url = uritemplate.expand(DISCOVERY_URI,
                                       {'api': api, 'apiVersion': version})
    resp, content = httplib2.Http().request(requested_url)
    if resp.status >= 400:
        raise HttpError(resp, content, uri=requested_url)
    try:
        with open(path, 'w') as discovery_doc:
            discovery_json = json.loads(content)
            json.dump(discovery_json, discovery_doc)
    except ValueError:
        raise InvalidJsonError(
            'Bad JSON: %s from %s.' % (content, requested_url))
# [END build_and_update]
