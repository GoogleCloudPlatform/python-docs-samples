#!/usr/bin/env python

# Copyright 2018 LLC
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
custom roles.

For more information, see the documentation at
https://cloud.google.com/iam/docs/creating-custom-roles.
"""

import argparse
import os

from google.oauth2 import service_account  # type: ignore
import googleapiclient.discovery  # type: ignore

credentials = service_account.Credentials.from_service_account_file(
    filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
    scopes=['https://www.googleapis.com/auth/cloud-platform'])
service = googleapiclient.discovery.build(
    'iam', 'v1', credentials=credentials)


# [START iam_query_testable_permissions]
def query_testable_permissions(resource: str) -> None:
    """Lists valid permissions for a resource."""

    # pylint: disable=no-member
    permissions = service.permissions().queryTestablePermissions(body={
        'fullResourceName': resource
    }).execute()['permissions']
    for p in permissions:
        print(p['name'])
# [END iam_query_testable_permissions]


# [START iam_get_role]
def get_role(name: str) -> None:
    """Gets a role."""

    # pylint: disable=no-member
    role = service.roles().get(name=name).execute()
    print(role['name'])
    for permission in role['includedPermissions']:
        print(permission)
# [END iam_get_role]


# [START iam_create_role]
def create_role(name: str, project: str, title: str, description: str, permissions: str, stage: str) -> dict:
    """Creates a role."""

    # pylint: disable=no-member
    role = service.projects().roles().create(
        parent='projects/' + project,
        body={
            'roleId': name,
            'role': {
                'title': title,
                'description': description,
                'includedPermissions': permissions,
                'stage': stage
            }
        }).execute()

    print('Created role: ' + role['name'])
    return role
# [END iam_create_role]


# [START iam_edit_role]
def edit_role(name: str, project: str, title: str, description: str, permissions: str, stage: str) -> dict:
    """Creates a role."""

    # pylint: disable=no-member
    role = service.projects().roles().patch(
        name='projects/' + project + '/roles/' + name,
        body={
            'title': title,
            'description': description,
            'includedPermissions': permissions,
            'stage': stage
        }).execute()

    print('Updated role: ' + role['name'])
    return role
# [END iam_edit_role]


# [START iam_list_roles]
def list_roles(project_id: str) -> None:
    """Lists roles."""

    # pylint: disable=no-member
    roles = service.roles().list(
        parent='projects/' + project_id).execute()['roles']
    for role in roles:
        print(role['name'])
# [END iam_list_roles]


# [START iam_disable_role]
def disable_role(name: str, project: str) -> dict:
    """Disables a role."""

    # pylint: disable=no-member
    role = service.projects().roles().patch(
        name='projects/' + project + '/roles/' + name,
        body={
            'stage': 'DISABLED'
        }).execute()

    print('Disabled role: ' + role['name'])
    return role
# [END iam_disable_role]


# [START iam_delete_role]
def delete_role(name: str, project: str) -> dict:
    """Deletes a role."""

    # pylint: disable=no-member
    role = service.projects().roles().delete(
        name='projects/' + project + '/roles/' + name).execute()

    print('Deleted role: ' + name)
    return role
# [END iam_delete_role]


# [START iam_undelete_role]
def undelete_role(name: str, project: str) -> dict:
    """Undeletes a role."""

    # pylint: disable=no-member
    role = service.projects().roles().patch(
        name='projects/' + project + '/roles/' + name,
        body={
            'stage': 'DISABLED'
        }).execute()

    print('Disabled role: ' + role['name'])
    return role
# [END iam_undelete_role]


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(dest='command')

    # Permissions
    view_permissions_parser = subparsers.add_parser(
        'permissions', help=query_testable_permissions.__doc__)
    view_permissions_parser.add_argument('resource')

    # Get
    get_role_parser = subparsers.add_parser('get', help=get_role.__doc__)
    get_role_parser.add_argument('name')

    # Create
    get_role_parser = subparsers.add_parser('create', help=create_role.__doc__)
    get_role_parser.add_argument('name')
    get_role_parser.add_argument('project')
    get_role_parser.add_argument('title')
    get_role_parser.add_argument('description')
    get_role_parser.add_argument('permissions')
    get_role_parser.add_argument('stage')

    # Edit
    edit_role_parser = subparsers.add_parser('edit', help=create_role.__doc__)
    edit_role_parser.add_argument('name')
    edit_role_parser.add_argument('project')
    edit_role_parser.add_argument('title')
    edit_role_parser.add_argument('description')
    edit_role_parser.add_argument('permissions')
    edit_role_parser.add_argument('stage')

    # List
    list_roles_parser = subparsers.add_parser('list', help=list_roles.__doc__)
    list_roles_parser.add_argument('project_id')

    # Disable
    disable_role_parser = subparsers.add_parser(
        'disable', help=get_role.__doc__)
    disable_role_parser.add_argument('name')
    disable_role_parser.add_argument('project')

    # Delete
    delete_role_parser = subparsers.add_parser('delete', help=get_role.__doc__)
    delete_role_parser.add_argument('name')
    delete_role_parser.add_argument('project')

    # Undelete
    undelete_role_parser = subparsers.add_parser(
        'undelete', help=get_role.__doc__)
    undelete_role_parser.add_argument('name')
    undelete_role_parser.add_argument('project')

    args = parser.parse_args()

    if args.command == 'permissions':
        query_testable_permissions(args.resource)
    elif args.command == 'get':
        get_role(args.name)
    elif args.command == 'list':
        list_roles(args.project_id)
    elif args.command == 'create':
        create_role(
            args.name, args.project, args.title,
            args.description, args.permissions, args.stage)
    elif args.command == 'edit':
        edit_role(
            args.name, args.project, args.title,
            args.description, args.permissions, args.stage)
    elif args.command == 'disable':
        disable_role(args.name, args.project)
    elif args.command == 'delete':
        delete_role(args.name, args.project)
    elif args.command == 'undelete':
        undelete_role(args.name, args.project)


if __name__ == '__main__':
    main()
