#!/usr/bin/env python

# Copyright 2018 Google Inc. All Rights Reserved.
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


def quickstart():
    # [START iam_quickstart]
    import os

    from google.oauth2 import service_account
    import googleapiclient.discovery

    # Get credentials
    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    # Create the Cloud IAM service object
    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)

    # Call the Cloud IAM Roles API
    # If using pylint, disable weak-typing warnings
    # pylint: disable=no-member
    response = service.roles().list().execute()
    roles = response['roles']

    # Process the response
    for role in roles:
        print('Title: ' + role['title'])
        print('Name: ' + role['name'])
        if 'description' in role:
            print('Description: ' + role['description'])
        print('')
    # [END iam_quickstart]


if __name__ == '__main__':
    quickstart()
