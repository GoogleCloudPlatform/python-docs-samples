#!/usr/bin/env python3

import argparse
import inspect
import os
import sys
from datetime import datetime

import helpers
from commands import (
    project_exists,
    use_service_account,
    has_file,
    simulation_mode_disclaimer,
    use_service_account_disclaimer
)
from connector import main_connector


def create_parser():
    """CLI parser."""
    parser_local = argparse.ArgumentParser(
        description='Run setup on projects of a organization.')

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

    parser_local.add_argument('-k',
                              '--key_file',
                              help='Service Account Key File',
                              dest='key_file',
                              required=True)

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

    parser_local.add_argument('-r',
                              '--region',
                              help='Region',
                              dest='region',
                              required=True)

    parser_local.add_argument('-rg',
                              '--gae_region',
                              help='Google app engine Region',
                              dest='gae_region',
                              required=True)

    parser_local.add_argument('-cp',
                              '--connector_project',
                              help='Connector project id',
                              dest='connector_project',
                              required=True)

    parser_local.add_argument('-cb',
                              '--connector_bucket',
                              help='Connector bucket',
                              dest='connector_bucket',
                              required=True)

    parser_local.add_argument('-cfb',
                              '--cf_bucket',
                              help='Cloud Function Bucket',
                              dest='cf_bucket',
                              required=True)

    parser_local.add_argument('-csa',
                              '--connector_sa_file',
                              help='Connector service account file full path.',
                              dest='connector_sa_file',
                              required=True)

    parser_local.add_argument('-q',
                              '--quiet',
                              help='disable all interactive prompts when running',
                              dest='quiet',
                              action='store_true')

    parser_local.set_defaults(dry_run=True)
    parser_local.set_defaults(quiet=False)
    parser_local.set_defaults(notifier_skip_pubsub=False)

    return parser_local


def validate_arguments(args):

    if not has_file(args.key_file):
        print('Key File Does not Exist.\nPlease inform a file.')
        sys.exit(1)

    if not project_exists(args.connector_project):
        print(('Project {} not found. Please check if id is correct or if you '
               'have been granted access to it.'.format(args.connector_project)))
        sys.exit(2)

    connector_sa_file = args.connector_sa_file
    if connector_sa_file and not os.path.isfile(connector_sa_file):
        print('The service account file path passed is not valid: "{}".'.format(
            connector_sa_file))
        sys.exit(4)


def run_steps(args):
    helpers_config(args)
    validate_arguments(args)
    simulation_mode_disclaimer()
    use_service_account(args.key_file)
    main_connector(args)
    simulation_mode_disclaimer()
    use_service_account_disclaimer()


def helpers_config(args):
    helpers.START_TIME = datetime.utcnow().strftime('%Y%m%d%H%M')
    helpers.DRY_RUN = args.dry_run
    helpers.BASE_DIR = os.path.join(os.path.dirname(
        os.path.abspath(inspect.stack()[0][1])), '..')


def writer_task(args):
    print('connector task.')
    main_connector(args)


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    run_steps(args)
