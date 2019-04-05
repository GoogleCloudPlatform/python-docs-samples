#!/usr/bin/env python3

import argparse
import inspect
from datetime import datetime
import os
import sys
import re

import helpers
from base import run_command


def create_parser():
    """CLI parser."""
    parser_local = argparse.ArgumentParser(
        description='Grant roles to member from project or organization.')

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

    parser_local.add_argument('-o',
                              '--organization_id',
                              help='Organization ID',
                              dest='organization_id')

    parser_local.add_argument('-p',
                              '--project_id',
                              help='Project ID',
                              dest='project_id')

    parser_local.add_argument('-f',
                              '--file',
                              help='File with a list of curated roles to be associated',
                              dest='file',
                              required=True)

    parser_local.add_argument('-c',
                              '--credential_file',
                              help='Service account credential json file',
                              dest='credential_file')

    parser_local.add_argument('-s',
                              '--sa_email',
                              help='Service account email',
                              dest='sa_email')

    parser_local.add_argument('-u',
                              '--user_email',
                              help='User email',
                              dest='user_email')

    parser_local.add_argument('-g',
                              '--group_email',
                              help='Group email',
                              dest='group_email')

    parser_local.set_defaults(dry_run=True)
    return parser_local


def validate_arguments(args):
    if (not args.organization_id and not args.project_id):
        print('Please provide the project OR organization id.')
        sys.exit(1)

    if (not os.path.isfile(args.file)):
        print('Missing set of roles for [{}]'.format(args.file))
        sys.exit(2)

    if (not args.credential_file and
        not args.sa_email and
        not args.user_email and
            not args.group_email):
        print('Please provide the credential file OR service account email '
              'OR user email OR group email.')
        sys.exit(3)

    if (args.credential_file and not os.path.isfile(args.credential_file)):
        print('Service account [{}] not found.'.format(args.credential_file))
        sys.exit(4)


def helpers_config(args):
    helpers.START_TIME = datetime.utcnow().strftime('%Y%m%d%H%M')
    helpers.DRY_RUN = args.dry_run
    helpers.BASE_DIR = os.path.join(os.path.dirname(
        os.path.abspath(inspect.stack()[0][1])), '..')


def grant_roles_on_organization(role_file, organization_id, member_to_receive_grant):
    roles = None
    with open(role_file) as f:
        roles = f.readlines()
    for role in roles:
        cmd = [
            'gcloud', 'organizations',
            'add-iam-policy-binding', organization_id,
            '--member=' + member_to_receive_grant,
            '--role=' + role,
            '--quiet'
        ]
        run_command(cmd)


def grant_roles_on_project(role_file, project_id, member_to_receive_grant):
    roles = None
    with open(role_file) as f:
        roles = f.readlines()
    for role in roles:
        cmd = [
            'gcloud', 'projects',
            'add-iam-policy-binding', project_id,
            '--project', project_id,
            '--member=' + member_to_receive_grant,
            '--role=' + role,
            '--quiet'
        ]
        run_command(cmd)


def grant_roles(args):
    member_to_receive_grant = None
    if (args.credential_file):
        p = re.compile('\"client_email\": \"(.+?)\"', flags=re.MULTILINE)
        with open(args.credential_file) as f:
            m = p.search(f.read())
            if m:
                member_to_receive_grant = 'serviceAccount:' + m.group(1)
            else:
                print('Invalid service account file [{}].'
                      .format(args.credential_file))
                sys.exit(5)
    elif (args.sa_email):
        member_to_receive_grant = 'serviceAccount:' + args.sa_email
    elif (args.user_email):
        member_to_receive_grant = 'user:' + args.user_email
    else:
        member_to_receive_grant = 'group:' + args.group_email

    if args.organization_id:
        grant_roles_on_organization(
            args.file, args.organization_id, member_to_receive_grant)
    else:
        grant_roles_on_project(args.file, args.project_id,
                               member_to_receive_grant)


if __name__ == '__main__':
    args = create_parser().parse_args()
    validate_arguments(args)
    helpers_config(args)
    grant_roles(args)
