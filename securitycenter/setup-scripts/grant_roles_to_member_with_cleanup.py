#!/usr/bin/env python3

import argparse
import logging

import helpers
from clean_staled_service_accounts import clean_services_account
from commands import save_json_file
from parser_arguments import add_simulation_arguments
from gcp_utils.service_accounts import (
    get_policies_organization,
    get_policies_project,
    add_member_to_police,
    set_police_on_organization,
    set_police_on_project,
    use_service_account
)


def create_set_policies_parser():
    """CLI cleanup project parser"""

    parser = argparse.ArgumentParser(
        description='Run setup on projects of a organization.')

    parser.add_argument(
        '-c',
        '--service_account_credential',
        help='service account credential json file',
        dest='service_account_credential')

    parser.add_argument(
        '-s',
        '--service_account_email',
        help='Service Account e-mail',
        dest='service_account_email')

    parser.add_argument(
        '-u',
        '--user_account_email',
        help='User Account e-mail',
        dest='user_account_email')

    parser.add_argument(
        '-g',
        '--group_account_email',
        help='Group Account e-mail',
        dest='group_account_email')

    parser.add_argument(
        '-f',
        '--file_roles',
        help='File with roles to be added',
        dest='roles_file',
        required=True)

    parser.add_argument(
        '-p',
        '--project_id',
        help='GCP project',
        dest='project_id')

    parser.add_argument(
        '-o',
        '--organization',
        help='Organization ID',
        dest='organization_id')

    parser.add_argument(
        '-CL',
        '--cleanup',
        help='Case true, cleanup old services accounts of informed organization',
        dest='cleanup',
        action='store_true')

    parser.set_defaults(dry_run=True)
    parser.set_defaults(cleanup=False)

    return parser


def add_roles_to_policies(members, roles, policies):
    for role in roles:
        for member in members:
            add_member_to_police(member, role, policies)


def add_roles_to_organization(
        organization_id, members, roles,
        original_organization_policies_file,
        new_organization_policies_file):
    organization_policies = get_policies_organization(organization_id)

    save_json_file(original_organization_policies_file, organization_policies)
    print("Original policies for organization saved at: {}"
          .format(original_organization_policies_file))

    add_roles_to_policies(members, roles, organization_policies)

    save_json_file(new_organization_policies_file, organization_policies)
    print("New policies for organization saved at: {}"
          .format(new_organization_policies_file))


def add_roles_to_project(project_id,
                         members,
                         roles,
                         original_project_policies_file,
                         new_project_policies_file):
    project_policies = get_policies_project(project_id)

    save_json_file(original_project_policies_file, project_policies)
    print("Original policies for project saved at: {}"
          .format(original_project_policies_file))

    add_roles_to_policies(members, roles, project_policies)

    save_json_file(new_project_policies_file, project_policies)
    print("New policies for project saved at: {}"
          .format(new_project_policies_file))


def main_set_policies():
    """Main set policies"""
    parser = create_set_policies_parser()
    add_simulation_arguments(parser)
    args = parser.parse_args()
    helpers.DRY_RUN = args.dry_run
    roles = roles_file_to_list(args.roles_file)
    set_policies(roles,
                 organization_id=args.organization_id,
                 project_id=args.project_id,
                 service_account_credential=args.service_account_credential,
                 service_account_email=args.service_account_email,
                 user_account_email=args.user_account_email,
                 group_account_email=args.group_account_email,
                 cleanup=args.cleanup)


def set_policies(roles,
                 organization_id=None, project_id=None,
                 service_account_credential=None,
                 service_account_email=None,
                 user_account_email=None,
                 group_account_email=None,
                 cleanup=False):
    if service_account_credential:
        use_service_account(service_account_credential)
    if cleanup:
        if organization_id:
            clean_services_account(organization_id)
        else:
            logging.error("The cleanup roles option "
                          "is available only to organizations!")
    if len(roles) == 0:
        logging.error("No roles to be granted!")
    else:
        members = build_members(service_account_email,
                                user_account_email,
                                group_account_email)
        if len(members) > 0:
            if organization_id:
                set_organization_policy(members, organization_id, roles)
            if project_id:
                set_project_policy(members, project_id, roles)
        else:
            logging.error("No member to grant role!")


def set_project_policy(members, project_id, roles):
    original_project_policies_file = "original_project_policies.json"
    new_project_policies_file = "new_project_policies_file.json"
    add_roles_to_project(project_id, members, roles,
                         original_project_policies_file,
                         new_project_policies_file)
    set_police_on_project(project_id, new_project_policies_file)


def set_organization_policy(members, organization_id, roles):
    original_org_policies_file = "original_organization_policies.json"
    new_org_policies_file = "new_organization_policies_file.json"
    add_roles_to_organization(organization_id,
                              members, roles,
                              original_org_policies_file,
                              new_org_policies_file)
    set_police_on_organization(organization_id,
                               new_org_policies_file)


def roles_file_to_list(roles_file):
    roles = [line.rstrip('\n') for line in open(roles_file)]
    return roles


def build_members(service_account_email,
                  user_account_email,
                  group_account_email):
    members = []
    if service_account_email:
        members.append("serviceAccount:" + service_account_email)
    if user_account_email:
        members.append("user:" + user_account_email)
    if group_account_email:
        members.append("group:" + group_account_email)
    return members


if __name__ == '__main__':
    main_set_policies()
