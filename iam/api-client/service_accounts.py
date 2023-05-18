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
"""Demonstrates how to perform basic operations with Google Cloud IAM
service accounts.
For more information, see the documentation at
https://cloud.google.com/iam/docs/creating-managing-service-accounts.
"""

import argparse
# [START iam_create_service_account]
# [START iam_list_service_accounts]
# [START iam_rename_service_account]
# [START iam_disable_service_account]
# [START iam_enable_service_account]
# [START iam_delete_service_account]
import os

from google.oauth2 import service_account  # type: ignore
import googleapiclient.discovery  # type: ignore

# [END iam_create_service_account]
# [END iam_list_service_accounts]
# [END iam_rename_service_account]
# [END iam_disable_service_account]
# [END iam_enable_service_account]
# [END iam_delete_service_account]


# [START iam_create_service_account]
def create_service_account(project_id: str, name: str, display_name: str) -> dict:
    """Creates a service account."""

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)

    my_service_account = service.projects().serviceAccounts().create(
        name='projects/' + project_id,
        body={
            'accountId': name,
            'serviceAccount': {
                'displayName': display_name
            }
        }).execute()

    print('Created service account: ' + my_service_account['email'])
    return my_service_account
# [END iam_create_service_account]


# [START iam_list_service_accounts]
def list_service_accounts(project_id: str) -> dict:
    """Lists all service accounts for the current project."""

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)

    service_accounts = service.projects().serviceAccounts().list(
        name='projects/' + project_id).execute()

    for account in service_accounts['accounts']:
        print('Name: ' + account['name'])
        print('Email: ' + account['email'])
        print(' ')
    return service_accounts
# [END iam_list_service_accounts]


# [START iam_rename_service_account]
def rename_service_account(email: str, new_display_name: str) -> dict:
    """Changes a service account's display name."""

    # First, get a service account using List() or Get()
    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)

    resource = 'projects/-/serviceAccounts/' + email

    my_service_account = service.projects().serviceAccounts().get(
        name=resource).execute()

    # Then you can update the display name
    my_service_account['displayName'] = new_display_name
    my_service_account = service.projects().serviceAccounts().update(
        name=resource, body=my_service_account).execute()

    print('Updated display name for {} to: {}'.format(
        my_service_account['email'], my_service_account['displayName']))
    return my_service_account
# [END iam_rename_service_account]


# [START iam_disable_service_account]
def disable_service_account(email: str) -> None:
    """Disables a service account."""

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)

    service.projects().serviceAccounts().disable(
        name='projects/-/serviceAccounts/' + email).execute()

    print("Disabled service account :" + email)
# [END iam_disable_service_account]


# [START iam_enable_service_account]
def enable_service_account(email: str) -> None:
    """Enables a service account."""

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)

    service.projects().serviceAccounts().enable(
        name='projects/-/serviceAccounts/' + email).execute()

    print("Enabled service account :" + email)
# [END iam_enable_service_account]


# [START iam_delete_service_account]
def delete_service_account(email: str) -> None:
    """Deletes a service account."""

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)

    service.projects().serviceAccounts().delete(
        name='projects/-/serviceAccounts/' + email).execute()

    print('Deleted service account: ' + email)
# [END iam_delete_service_account]


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(dest='command')

    # Create
    create_parser = subparsers.add_parser(
        'create', help=create_service_account.__doc__)
    create_parser.add_argument('project_id')
    create_parser.add_argument('name')
    create_parser.add_argument('display_name')

    # List
    list_parser = subparsers.add_parser(
        'list', help=list_service_accounts.__doc__)
    list_parser.add_argument('project_id')

    # Rename
    rename_parser = subparsers.add_parser(
        'rename', help=rename_service_account.__doc__)
    rename_parser.add_argument('email')
    rename_parser.add_argument('new_display_name')

    # Disable
    rename_parser = subparsers.add_parser(
        'disable', help=disable_service_account.__doc__)
    list_parser.add_argument('email')

    # Enable
    rename_parser = subparsers.add_parser(
        'enable', help=enable_service_account.__doc__)
    list_parser.add_argument('email')

    # Delete
    delete_parser = subparsers.add_parser(
        'delete', help=delete_service_account.__doc__)
    delete_parser.add_argument('email')

    args = parser.parse_args()

    if args.command == 'create':
        create_service_account(args.project_id, args.name, args.display_name)
    elif args.command == 'list':
        list_service_accounts(args.project_id)
    elif args.command == 'rename':
        rename_service_account(args.email, args.new_display_name)
    elif args.command == 'delete':
        delete_service_account(args.email)


if __name__ == '__main__':
    main()
