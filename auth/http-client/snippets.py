# Copyright 2016 Google Inc. All Rights Reserved.
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

"""Demonstrates how to authenticate to Google Cloud Platform APIs using the
Requests HTTP library."""

import argparse


def implicit():
    import google.auth
    from google.auth.transport import requests

    # Get the credentials and project ID from the environment.
    credentials, project = google.auth.default(
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    # Create a requests Session object with the credentials.
    session = requests.AuthorizedSession(credentials)

    # Make an authenticated API request
    response = session.get(
        'https://www.googleapis.com/storage/v1/b'.format(project),
        params={'project': project})
    response.raise_for_status()
    buckets = response.json()
    print(buckets)


def explicit(project):
    from google.auth.transport import requests
    from google.oauth2 import service_account

    # Construct service account credentials using the service account key
    # file.
    credentials = service_account.Credentials.from_service_account_file(
        'service_account.json')
    credentials = credentials.with_scopes(
        ['https://www.googleapis.com/auth/cloud-platform'])

    # Create a requests Session object with the credentials.
    session = requests.AuthorizedSession(credentials)

    # Make an authenticated API request
    response = session.get(
        'https://www.googleapis.com/storage/v1/b'.format(project),
        params={'project': project})
    response.raise_for_status()
    buckets = response.json()
    print(buckets)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('implicit', help=implicit.__doc__)
    explicit_parser = subparsers.add_parser('explicit', help=explicit.__doc__)
    explicit_parser.add_argument('project')

    args = parser.parse_args()

    if args.command == 'implicit':
        implicit()
    elif args.command == 'explicit':
        explicit(args.project)
