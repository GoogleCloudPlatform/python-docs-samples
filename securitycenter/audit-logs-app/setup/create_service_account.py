#!/usr/bin/env python3

import argparse
import inspect
import os

from datetime import datetime

import helpers
from base import run_command
from commands import (
    get_service_account_email,
    has_file,
    get_cloud_services_default_service_account
)


def create_parser():
    """CLI parser."""
    parser_local = argparse.ArgumentParser(
        description='Create service account with the roles passed.')

    parser_local.add_argument('-n',
                              '--name',
                              help='Service account name.',
                              dest='name',
                              required=True)

    parser_local.add_argument('-p',
                              '--project_id',
                              help='Project ID',
                              dest='project_id',
                              required=True)

    parser_local.add_argument('-o',
                              '--organization_id',
                              help='Organization ID',
                              dest='organization_id',
                              required=True)

    parser_local.add_argument('-rf',
                              '--roles_file',
                              help='File with roles',
                              dest='roles_file',
                              required=True)

    parser_local.add_argument('-S',
                              '--simulation',
                              help='Simulate the execution. Do not execute any command.',
                              dest='dry_run',
                              action='store_true')

    parser_local.add_argument('-NS',
                              '--no-simulation',
                              help='Really execute. Execute everything.',
                              dest='dry_run',
                              action='store_false')

    parser_local.set_defaults(dry_run=True)

    return parser_local


def create_sa(sa_name, project_id, organization_id, sa_roles):
    """Create service account with the roles passed.

    OBS: It also has the responsibility to:

     * enable required APIs in the project
     * apply roles to DM Google-managed service account

    Args:
        sa_name: Service account name.
        project_id: Project id.
        organization_id: Organization id.
        sa_roles: Roles to add to service account.

    Returns:
        The service account generated file name.
    """
    apis_to_enable = [
        'cloudbilling.googleapis.com',
        'cloudresourcemanager.googleapis.com',
        'deploymentmanager.googleapis.com',
        'iam.googleapis.com',
        'appengine.googleapis.com',
        'cloudbuild.googleapis.com',
        'cloudfunctions.googleapis.com',
        'servicemanagement.googleapis.com',
    ]
    for api in apis_to_enable:
        run_command([
            'gcloud', 'services', 'enable', api,
            '--project', args.project_id
        ])

    print('Roles to DM.')
    dm_roles = [
        'roles/billing.user',
        'roles/deploymentmanager.editor',
        'roles/resourcemanager.projectCreator',
        'roles/iam.organizationRoleAdmin',
        'roles/logging.admin'
    ]
    dm_email = get_cloud_services_default_service_account(args.project_id)
    for role in dm_roles:
        run_command([
            'gcloud', 'organizations', 'add-iam-policy-binding',
            args.organization_id,
            '--member', 'serviceAccount:' + dm_email,
            '--quiet',
            '--role', role
        ])

    sa_file_name = os.path.join(
        helpers.BASE_DIR,
        'setup',
        'service_accounts',
        project_id + '_' + sa_name + '.json')
    if not has_file(sa_file_name):
        run_command([
            'gcloud', 'iam', 'service-accounts', 'create', sa_name,
            '--display-name', sa_name,
            '--project', project_id
        ])
        account_email = get_service_account_email(sa_name, project_id)
        sa_directory = os.path.join(
            helpers.BASE_DIR, 'setup', 'service_accounts')
        if not os.path.exists(sa_directory):
            os.makedirs(sa_directory)
        run_command([
            'gcloud', 'iam', 'service-accounts', 'keys', 'create',
            sa_file_name,
            '--iam-account', account_email,
            '--project', project_id
        ])
        print('Roles to SA.')
        for role in sa_roles:
            run_command([
                'gcloud', 'organizations', 'add-iam-policy-binding',
                organization_id,
                '--member', 'serviceAccount:' + account_email,
                '--quiet',
                '--role', role
            ])
    return sa_file_name


def roles_file_to_list(roles_file):
    return [line.rstrip('\n') for line in open(roles_file)]


def helpers_config(args):
    helpers.START_TIME = datetime.utcnow().strftime('%Y%m%d%H%M')
    helpers.DRY_RUN = args.dry_run
    helpers.BASE_DIR = os.path.join(os.path.dirname(
        os.path.abspath(inspect.stack()[0][1])), '..')


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    helpers_config(args)
    roles = roles_file_to_list(args.roles_file)
    file_name = create_sa(args.name, args.project_id,
                          args.organization_id, roles)
    print('Service account created with file "{}".'.format(file_name))
