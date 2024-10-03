# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Anti Money Laundering AI sample for listing the Cloud locations
    of the API.
Example usage:
    python list_locations.py --project_id <project-id>
"""

# [START antimoneylaunderingai_list_locations]

import argparse
import os

import google.auth
from google.auth.transport import requests


def list_locations(
    project_id: str,
) -> google.auth.transport.Response:
    """Lists the AML AI locations using the REST API."""

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project' # The Google Cloud project ID.

    # Gets credentials from the environment. google.auth.default() returns credentials and the
    # associated project ID, but in this sample, the project ID is passed in manually.
    credentials, _ = google.auth.default(
        scopes=[
            "https://www.googleapis.com/auth/cloud-platform",
        ]
    )
    authed_session = requests.AuthorizedSession(credentials)

    # URL to the AML AI API endpoint and version
    base_url = "https://financialservices.googleapis.com/v1"
    url = f"{base_url}/projects/{project_id}/locations/"
    # Sets required "application/json" header on the request
    headers = {"Content-Type": "application/json; charset=utf-8"}

    response = authed_session.get(url, headers=headers)
    response.raise_for_status()
    print(response.text)
    return response


# [END antimoneylaunderingai_list_locations]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project_id",
        default=(os.environ.get("GOOGLE_CLOUD_PROJECT")),
        help="Google Cloud project name",
    )
    args = parser.parse_args()

    list_locations(
        args.project_id,
    )
