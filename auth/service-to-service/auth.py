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

"""
Demonstrates how to send authenticated service-to-service requests, eg
for Cloud Run or Cloud Functions"""

# [START google_auth_idtoken_serverless]
# [START functions_bearer_token]
# [START cloudrun_service_to_service_auth]
# [START run_service_to_service_auth]
import urllib

import google.auth.transport.requests
import google.oauth2.id_token


def make_authorized_get_request(service_url):
    """
    make_authorized_get_request makes a GET request to the specified HTTP endpoint
    in service_url (must be a complete URL) by authenticating with the
    ID token obtained from the google-auth client library.
    """

    req = urllib.request.Request(service_url)

    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, service_url)

    req.add_header("Authorization", f"Bearer {id_token}")
    response = urllib.request.urlopen(req)

    return response.read()
# [END run_service_to_service_auth]
# [END cloudrun_service_to_service_auth]
# [END functions_bearer_token]
# [END google_auth_idtoken_serverless]
