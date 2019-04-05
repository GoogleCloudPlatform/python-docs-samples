import argparse
import csv
import logging

import helpers
from base import run_command
from commands import save_json_file
from gcp_utils.projects import (
    get_json_list_projects,
    check_project_exists
)
from parser_arguments import add_simulation_arguments
from gcp_utils.service_accounts import (
    use_service_account,
    remove_from_police,
    set_police_on_organization,
    get_policies_organization,
    get_project_number,
    get_project_name
)

services_accounts_csv_file = "services_accounts.csv"

LOGGER = logging.getLogger(__name__)


def create_cleanup_services_accounts_parser():
    """
    CLI cleanup project parser
    """
    parser = argparse.ArgumentParser(
        description='Run setup on projects of a organization.')

    parser.add_argument(
        '-k',
        '--key_file',
        help='Service Account Key File',
        dest='key_file')

    parser.add_argument(
        '-o',
        '--organization_id',
        help='Organization ID',
        dest='organization_id',
        required=True)

    parser.add_argument(
        '-q',
        '--quiet',
        help='Disable all interactive prompts when running',
        dest='quiet',
        action='store_true')

    parser.set_defaults(dry_run=True)

    return parser


def get_services_accounts(organization_id):
    """
    Get services accounts
        :param organization_id: organization
    """
    LOGGER.info("Getting services accounts")
    data = run_command([
        'gcloud', 'organizations', 'get-iam-policy', organization_id,
        "--flatten='bindings[]'",
        "--format='csv(bindings.members)'"
    ])
    if not helpers.DRY_RUN:
        with open(services_accounts_csv_file, 'wb') as output:
            output.write(data)
    else:
        with open(services_accounts_csv_file, 'wb') as output:
            output.write(b'deployer@control.iam.gserviceaccount.com')


def check_services_accounts_to_delete(organization_id, 
                                      original_policies_file, 
                                      new_policies_file):
    """
    Check services accounts to delete.
        :param organization_id: organization id
        :param original_policies_file: original policies
        :param new_policies_file: new policies
    """
    with open(services_accounts_csv_file, 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        members = list(reader)

    policies = get_policies_organization(organization_id)
    save_json_file(original_policies_file, policies)
    LOGGER.info("Backup police file saved as: " + original_policies_file)

    projects_list = get_json_list_projects("", "", organization_id)

    for group in members:
        group_members = group[0].split(';')
        for member in group_members:
            if member.startswith('serviceAccount'):
                project_name = get_project_name(member)
                project_number = get_project_number(member)
                if (not check_project_exists(project_name, project_number,
                                             projects_list)):
                    LOGGER.info("Deleting " + member)
                    remove_from_police(member, policies)

    save_json_file(new_policies_file, policies)
    LOGGER.info("New police file saved as: " + new_policies_file)


def clean_services_account(organization_id):
    """
    Remove permissions from services account of projects that are not visible
    or have been deleted. This method is destructive. Use with caution.
        :param organization_id: organization id
    """
    print(
        "Cleanup old services accounts to organization " + str(organization_id))
    original_policies_file = "original_organization_policies.json"
    new_policies_file = "new_organization_policies_file.json"

    get_services_accounts(organization_id)
    check_services_accounts_to_delete(organization_id, original_policies_file,
                                      new_policies_file)
    set_police_on_organization(organization_id, new_policies_file)


def main_cleanup_services_accounts():
    """
    CLI entry point.
    """
    parser = create_cleanup_services_accounts_parser()
    add_simulation_arguments(parser)
    args = parser.parse_args()
    helpers.DRY_RUN = args.dry_run

    if args.key_file:
        use_service_account(args.key_file)

    clean_services_account(args.organization_id)


if __name__ == '__main__':
    main_cleanup_services_accounts()