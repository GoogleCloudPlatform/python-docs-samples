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

import argparse
import os

from google.oauth2 import service_account  # type: ignore
import googleapiclient.discovery  # type: ignore

credentials = service_account.Credentials.from_service_account_file(
    filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
    scopes=['https://www.googleapis.com/auth/cloud-platform'])
service = googleapiclient.discovery.build(
    'iam', 'v1', credentials=credentials)


# [START iam_view_grantable_roles]
def view_grantable_roles(full_resource_name: str) -> None:
    roles = service.roles().queryGrantableRoles(body={
        'fullResourceName': full_resource_name
    }).execute()

    for role in roles['roles']:
        if 'title' in role:
            print('Title: ' + role['title'])
        print('Name: ' + role['name'])
        if 'description' in role:
            print('Description: ' + role['description'])
        print(' ')
# [END iam_view_grantable_roles]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'full_resource_name',
        help='The full name of the resource to query grantable roles for.')

    args = parser.parse_args()
    view_grantable_roles(args.full_resource_name)
