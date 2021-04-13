# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Get the client ID associated with a Cloud Composer environment."""

import argparse


def get_client_id(project_id, location, composer_environment):
    # [START composer_get_environment_client_id]
    import google.auth
    import google.auth.transport.requests
    import requests
    import six.moves.urllib.parse

    # Authenticate with Google Cloud.
    # See: https://cloud.google.com/docs/authentication/getting-started
    credentials, _ = google.auth.default(
        scopes=['https://www.googleapis.com/auth/cloud-platform'])
    authed_session = google.auth.transport.requests.AuthorizedSession(
        credentials)

    # project_id = 'YOUR_PROJECT_ID'
    # location = 'us-central1'
    # composer_environment = 'YOUR_COMPOSER_ENVIRONMENT_NAME'

    environment_url = (
        'https://composer.googleapis.com/v1beta1/projects/{}/locations/{}'
        '/environments/{}').format(project_id, location, composer_environment)
    composer_response = authed_session.request('GET', environment_url)
    environment_data = composer_response.json()
    airflow_uri = environment_data['config']['airflowUri']

    # The Composer environment response does not include the IAP client ID.
    # Make a second, unauthenticated HTTP request to the web server to get the
    # redirect URI.
    redirect_response = requests.get(airflow_uri, allow_redirects=False)
    redirect_location = redirect_response.headers['location']

    # Extract the client_id query parameter from the redirect.
    parsed = six.moves.urllib.parse.urlparse(redirect_location)
    query_string = six.moves.urllib.parse.parse_qs(parsed.query)
    print(query_string['client_id'][0])
    # [END composer_get_environment_client_id]


# Usage: python get_client_id.py your_project_id your_region your_environment_name
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', help='Your Project ID.')
    parser.add_argument(
        'location', help='Region of the Cloud Composer environment.')
    parser.add_argument(
        'composer_environment', help='Name of the Cloud Composer environment.')

    args = parser.parse_args()
    get_client_id(
        args.project_id, args.location, args.composer_environment)
