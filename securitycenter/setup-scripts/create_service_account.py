#!/usr/bin/env python3

import argparse
import inspect
import logging
import os
import sys
import time
from datetime import datetime

import helpers
from base import run_command
from commands import (
    has_file,
    build_org_level_role_full_name,
    iam_org_level_role_exist
)
from grant_roles_to_member_with_cleanup import set_policies
from parser_arguments import add_simulation_arguments

LOGGER = logging.getLogger(__name__)


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
                              required=False)

    parser_local.add_argument('-rf',
                              '--roles_file',
                              help='File with roles',
                              dest='roles_file')

    parser_local.add_argument('-of',
                              '--output_file',
                              help='Output service account file path',
                              dest='output_file')

    parser_local.add_argument('-cr',
                              '--custom_roles',
                              help='Comma separated values for custom roles',
                              dest='custom_roles')

    parser_local.set_defaults(dry_run=True)

    return parser_local


def create_sa(args):
    """Create service account with the roles passed."""
    sa_file_name = args.output_file or os.path.join(
        helpers.BASE_DIR,
        'setup',
        'service_accounts',
        '{}_{}.json'.format(args.project_id, args.name))
    if has_file(sa_file_name):
        LOGGER.info('Service account file already exists on "%s".', sa_file_name)
        return
    else:
        run_command([
            'gcloud', 'iam', 'service-accounts', 'create', args.name,
            '--display-name', args.name,
            '--project', args.project_id
        ])
        time.sleep(5) #wait for data replication
        account_email = get_service_account_email_from_api(
            args.name, args.project_id)
        sa_directory = os.path.dirname(sa_file_name)
        if not os.path.exists(sa_directory):
            os.makedirs(sa_directory)
        run_command([
            'gcloud', 'iam', 'service-accounts', 'keys', 'create',
            sa_file_name,
            '--iam-account', account_email,
            '--project', args.project_id
        ])
        if args.roles_file:
            LOGGER.info('Roles to SA.')
            sa_roles = roles_file_to_list(args.roles_file)
            custom_roles = args.custom_roles
            if args.organization_id:
                if custom_roles:
                    LOGGER.info('Considering custom roles: %s', custom_roles)
                    custom_roles_list = custom_roles.split(',')
                    for custom_role in custom_roles_list:
                        full_custom_role = build_org_level_role_full_name(
                            args.organization_id, custom_role)
                        sa_roles.append(full_custom_role)
                set_policies(sa_roles,
                            organization_id=args.organization_id,
                            service_account_email=account_email)
            else:
                set_policies(sa_roles,
                            project_id=args.project_id,
                            service_account_email=account_email)
        LOGGER.info('Service account created with file "%s".', sa_file_name)


def helpers_config(args):
    helpers.START_TIME = datetime.utcnow().strftime('%Y%m%d%H%M')
    helpers.DRY_RUN = args.dry_run
    helpers.BASE_DIR = os.path.join(os.path.dirname(
        os.path.abspath(inspect.stack()[0][1])), '..')


def roles_file_to_list(roles_file):
    roles = [line.rstrip('\n') for line in open(roles_file)]
    return roles


def validate_arguments(args):
    roles_file = args.roles_file
    if roles_file and not has_file(roles_file):
        LOGGER.error('Role file passed is invalid: %s', roles_file)
        sys.exit(1)

    custom_roles = args.custom_roles
    if custom_roles:
        custom_roles_list = custom_roles.split(',')
        for custom_role in custom_roles_list:
            if not iam_org_level_role_exist(args.organization_id,
                                            custom_role):
                LOGGER.error('Custom role invalid or inexistent: %s',
                             custom_role)
                sys.exit(1)


def get_service_account_email_from_api(sa_name, project_id):
    account_email = run_command([
        'gcloud', 'iam service-accounts', 'list',
        '--project', project_id,
        '--filter', sa_name,
        '--format', 'value(email)'
    ])
    if helpers.DRY_RUN:
        return "creator@project_id.iam.gserviceaccount.com"
    else:
        return account_email.decode("utf-8").strip()


if __name__ == '__main__':
    parser = create_parser()
    add_simulation_arguments(parser)
    args = parser.parse_args()
    validate_arguments(args)
    helpers_config(args)
    create_sa(args)
