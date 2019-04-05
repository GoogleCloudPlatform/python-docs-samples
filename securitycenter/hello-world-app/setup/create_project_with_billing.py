#!/usr/bin/env python3

import argparse
import inspect
import sys
import os
from datetime import datetime

import helpers
from base import run_command, run_command_readonly
from commands import project_exists, simulation_mode_disclaimer


def create_parser():
    """CLI parser."""
    parser_local = argparse.ArgumentParser(
        description='Creates a project with billing passed on organization.')

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
                              dest='organization_id',
                              required=True)

    parser_local.add_argument('-b',
                              '--billing_account_id',
                              help='Billing account',
                              dest='billing_account_id',
                              required=True)

    parser_local.add_argument('-p',
                              '--project_id',
                              help='Project ID',
                              dest='project_id',
                              required=True)

    parser_local.set_defaults(dry_run=True)

    return parser_local


def validate_arguments(args):
    max_project_id_size = 30
    if len(args.project_id) > max_project_id_size:
        print('The project name is larger than the maximum size of ' +
              str(max_project_id_size))
        sys.exit(1)


def create_project(project_id, organization_id, billing_account_id):
    if project_exists(project_id):
        print('Project {} already exists.'.format(project_id))
        if not project_has_billing(project_id):
            print('Billing already enabled.')
        else:
            link_billing(billing_account_id, project_id)
    else:
        print('creating project {}.'.format(project_id))
        cmd = [
            'gcloud', 'projects', 'create', project_id,
            '--organization', organization_id
        ]
        run_command(cmd)
        link_billing(billing_account_id, project_id)


def link_billing(billing_account_id, project_id):
    print('Enabling billing for project {}.'.format(project_id))
    cmd = [
        'gcloud', 'beta', 'billing', 'projects', 'link', project_id,
        '--billing-account', billing_account_id
    ]
    run_command(cmd)


def project_has_billing(project_id):
    result = run_command_readonly([
        'gcloud', 'beta', 'billing', 'projects', 'describe', project_id,
         '--format', 'value(billingEnabled)'
    ])
    return 'TRUE' != result.decode("utf-8").strip().upper()


def helpers_config(args):
    helpers.START_TIME = datetime.utcnow().strftime('%Y%m%d%H%M')
    helpers.DRY_RUN = args.dry_run
    helpers.BASE_DIR = os.path.join(os.path.dirname(
        os.path.abspath(inspect.stack()[0][1])), '..')


def run_steps(args):
    validate_arguments(args)
    helpers_config(args)
    simulation_mode_disclaimer()
    create_project(
        args.project_id,
        args.organization_id,
        args.billing_account_id
    )
    simulation_mode_disclaimer()


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    validate_arguments(args)
    run_steps(args)
