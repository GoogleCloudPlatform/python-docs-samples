# Copyright 2020 Google, LLC.
#
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

import os
import urllib


METADATA_URL = 'http://metadata.google.internal/computeMetadata/v1/'
METADATA_HEADERS = {'Metadata-Flavor': 'Google'}


def new_request(data):
    """
    new_request creates a new HTTP request with IAM ID Token credential.
    This token is automatically handled by private Cloud Run (fully managed)
    and Cloud Functions.
    """

    url = os.environ.get('EDITOR_UPSTREAM_RENDER_URL')
    unauthenticated = os.environ.get('EDITOR_UPSTREAM_UNAUTHENTICATED')

    req = urllib.request.Request(url, data=data.encode())

    if not unauthenticated:
        token = get_token(url)
        req.add_header("Authorization", f"Bearer {token}")

    response = urllib.request.urlopen(req)
    return response.read()


def get_token(url):
    """
    Retrieves the IAM ID Token credential for the url.
    """
    token_url = (f"{METADATA_URL}instance/service-accounts/"
                 f"default/identity?audience={url}")
    token_req = urllib.request.Request(token_url, headers=METADATA_HEADERS)
    token_response = urllib.request.urlopen(token_req)
    token = token_response.read()
    return token.decode()
