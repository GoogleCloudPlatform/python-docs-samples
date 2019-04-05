import argparse
import inspect
import logging
import os
import sys
from datetime import datetime

import helpers
from commands import (
    has_file,
    iam_org_level_role_exist,
    get_cloud_services_default_service_account
)
from gcp_utils.base import scape_to_os, run_command
from parser_arguments import add_simulation_arguments

LOGGER = logging.getLogger(__name__)


def create_parser():
    """CLI parser."""
    parser_local = argparse.ArgumentParser(
        description='Create service account with the roles passed.')

    parser_local.add_argument('-n',
                              '--custom_role_name',
                              help='Name of the custom role',
                              dest='custom_role_name',
                              required=True)

    parser_local.add_argument('-d',
                              '--deployment_name',
                              help='Name for the deployment manager deployment',
                              dest='deployment_name',
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

    parser_local.add_argument('-t',
                              '--template_file',
                              help='Deployment Manager template file',
                              dest='template_file',
                              required=True)

    parser_local.set_defaults(dry_run=True)

    return parser_local


def validate_arguments(args):
    template_file = args.template_file
    if template_file and not has_file(template_file):
        LOGGER.error('Template file passed is invalid: %s', template_file)
        sys.exit(1)


def helpers_config(args):
    helpers.START_TIME = datetime.utcnow().strftime('%Y%m%d%H%M')
    helpers.DRY_RUN = args.dry_run
    helpers.BASE_DIR = os.path.join(os.path.dirname(
        os.path.abspath(inspect.stack()[0][1])), '..')


def create_role(args):
    if not iam_org_level_role_exist(args.organization_id,
                                    args.custom_role_name):
        apis_to_enable = [
            'cloudresourcemanager.googleapis.com',
            'deploymentmanager.googleapis.com',
            'iam.googleapis.com'
        ]
        for api in apis_to_enable:
            run_command([
                'gcloud', 'services', 'enable', api,
                '--project', args.project_id
            ])

        print('Roles to DM.')
        dm_roles = [
            'roles/deploymentmanager.editor',
            'roles/iam.organizationRoleAdmin',
        ]
        dm_email = get_cloud_services_default_service_account(
            args.project_id)
        for role in dm_roles:
            run_command([
                'gcloud', 'organizations', 'add-iam-policy-binding',
                args.organization_id,
                '--member', 'serviceAccount:' + dm_email,
                '--quiet',
                '--role', role
            ])

        deployment_name = args.deployment_name
        template_file = args.template_file
        cmd = [
            'gcloud', 'deployment-manager', 'deployments', 'create',
            deployment_name,
            '--template', template_file,
            '--properties',
            ",".join([
                'organizationId:' + scape_to_os(args.organization_id),
                ]),
            '--project', args.project_id]
        run_command(cmd)
    else:
        print('Custom role, CR - Google App Engine Application Creator, '
              'already exists.')


if __name__ == '__main__':
    parser = create_parser()
    add_simulation_arguments(parser)
    app_args = parser.parse_args()
    validate_arguments(app_args)
    helpers_config(app_args)
    create_role(app_args)
