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
from urllib import request


METADATA_URL = 'http://metadata.google.internal/computeMetadata/v1/'
METADATA_HEADERS = {'Metadata-Flavor': 'Google'}


class RenderService(object):
    """
    RenderService represents our upstream render service.
    """

    def __init__(self, URL, Authenticated):
        # URL is the render service address.
        self.url = URL
        # Auth determines whether identity token authentication will be used.
        self.authenticated = Authenticated


def new_request(RenderService):
    """
    new_request creates a new HTTP request with IAM ID Token credential.
    This token is automatically handled by private Cloud Run (fully managed)
    and Cloud Functions.
    """
    req = request.Request(RenderService.url)

    if not RenderService.authenticated:
        response = urllib.request.urlopen(req)

    token_url = (
        f"{METADATA_URL}instance/service-accounts/"
        f"default/identity?audience={RenderService.url}")
    token_req = request.Request(token_url, headers=METADATA_HEADERS)
    token_response = request.urlopen(token_req)
    token = token_response.read()

    return token


def render(RenderService):
    """
    render converts the Markdown plaintext to HTML.
    """
    req = new_request(RenderService)
    response = urllib.request.urlopen(req)
    return response




