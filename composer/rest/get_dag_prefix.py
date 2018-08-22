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

"""Get a Cloud Composer environment via the REST API.

This code sample gets a Cloud Composer environment resource and prints the
Cloud Storage path used to store Apache Airflow DAGs.
"""

import argparse


def get_dag_prefix(project_id, location, composer_environment):
    # [START composer_get_environment_dag_prefix]
    import google.auth
    import google.auth.transport.requests

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
    response = authed_session.request('GET', environment_url)
    environment_data = response.json()

    # Print the bucket name from the response body.
    print(environment_data['config']['dagGcsPrefix'])
    # [END composer_get_environment_dag_prefix]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', help='Your Project ID.')
    parser.add_argument(
        'location', help='Region of the Cloud Composer environent.')
    parser.add_argument(
        'composer_environment', help='Name of the Cloud Composer environent.')

    args = parser.parse_args()
    get_dag_prefix(
        args.project_id, args.location, args.composer_environment)
