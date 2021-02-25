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

# [START cloudrun_secure_request]
# [START run_secure_request]
import os
import urllib

import google.auth.transport.requests
import google.oauth2.id_token


def new_request(data):
    """
    new_request creates a new HTTP request with IAM ID Token credential.
    This token is automatically handled by private Cloud Run (fully managed)
    and Cloud Functions.
    """

    url = os.environ.get("EDITOR_UPSTREAM_RENDER_URL")
    if not url:
        raise Exception("EDITOR_UPSTREAM_RENDER_URL missing")

    req = urllib.request.Request(url, data=data.encode())
    auth_req = google.auth.transport.requests.Request()
    target_audience = url

    id_token = google.oauth2.id_token.fetch_id_token(auth_req, target_audience)
    req.add_header("Authorization", f"Bearer {id_token}")

    response = urllib.request.urlopen(req)
    return response.read()
# [END run_secure_request]
# [END cloudrun_secure_request]
