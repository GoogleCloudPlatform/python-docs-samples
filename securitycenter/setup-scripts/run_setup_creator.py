#!/usr/bin/env python3

import argparse
import inspect
import os
import sys
from commands import (has_file, project_exists, simulation_mode_disclaimer,
                      use_service_account, use_service_account_disclaimer)
from datetime import datetime

import helpers
from creator import (main_creator, main_creator_commands)


def create_parser():
    parser_local = argparse.ArgumentParser(description='Run setup on projects of a organization.')

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

    parser_local.add_argument('-cp',
                              '--creator_project',
                              help='Creator project name',
                              dest='creator_project_name',
                              required=True)

    parser_local.add_argument('-csa',
                              '--creator_sa_file',
                              help='Creator service account file full path.',
                              dest='creator_sa_file',
                              required=True)

    parser_local.add_argument('-psa',
                              '--publisher_sa_file',
                              help='Publisher service account file full path.',
                              dest='publisher_sa_file',
                              required=True)

    parser_local.add_argument('-sak',
                              '--scc_api_key',
                              help='scc api key to acces its functions',
                              dest='scc_api_key',
                              required=True)

    parser_local.add_argument('-q',
                              '--quiet',
                              help='disable all interactive prompts when running',
                              dest='quiet',
                              action='store_true')

    parser_local.add_argument('-dm',
                              '--use_dm',
                              help='Use Deployment Manager for the installation process',
                              dest='use_dm',
                              action='store_true')

    parser_local.set_defaults(dry_run=True)
    parser_local.set_defaults(quiet=False)
    parser_local.set_defaults(notifier_skip_pubsub=False)

    return parser_local


def validate_arguments(args):
    if not project_exists(args.creator_project_name):
        print('The creator project {} does not exist'.format(args.creator_project_name))
        sys.exit(2)

    creator_sa_file = args.creator_sa_file
    if creator_sa_file and not os.path.isfile(creator_sa_file):
        print('The service account file path passed is not valid: "{}".'.format(creator_sa_file))
        sys.exit(4)

    publisher_sa_file = args.publisher_sa_file
    if publisher_sa_file and not os.path.isfile(publisher_sa_file):
        print('The service account file path passed is not valid: "{}".'.format(publisher_sa_file))
        sys.exit(4)

def helpers_config(args):
    helpers.START_TIME = datetime.utcnow().strftime('%Y%m%d%H%M')
    helpers.DRY_RUN = args.dry_run
    helpers.BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), '..')


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    helpers_config(args)

    simulation_mode_disclaimer()

    validate_arguments(args)

    if args.use_dm:
        main_creator(args)
    else:
        main_creator_commands(args)
