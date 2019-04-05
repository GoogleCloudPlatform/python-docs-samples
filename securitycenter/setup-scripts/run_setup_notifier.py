#!/usr/bin/env python3

import argparse
import inspect
import os
import sys
from commands import (has_file, project_exists, simulation_mode_disclaimer,
                      use_service_account)
from datetime import datetime
from getpass import getuser

import helpers
from notifier import main_notifier, main_notifier_commands


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

    parser_local.add_argument('-o',
                              '--organization_id',
                              help='Organization ID',
                              dest='organization_id',
                              required=True)

    parser_local.add_argument('-r',
                              '--region',
                              help='Region',
                              dest='region',
                              required=True)

    parser_local.add_argument('-np',
                              '--notifier_project',
                              help='Notifier project id',
                              dest='notifier_project',
                              required=True)

    parser_local.add_argument('-nav',
                              '--notifier_appengine_version',
                              help='Notifier appengine version',
                              dest='notifier_appengine_version',
                              default=getuser())

    parser_local.add_argument('-nsp',
                              '--notifier_skip_pubsub',
                              help='Notifier skip pubsub',
                              dest='notifier_skip_pubsub',
                              action='store_true')

    parser_local.add_argument('-nhm',
                              '--notifier_hash_mecanism',
                              help='Notifier hash mecanism',
                              dest='notifier_hash_mecanism',
                              default='ON')

    parser_local.add_argument('-nb',
                              '--notifier_bucket',
                              help='Notifier cf bucket',
                              dest='notifier_bucket')

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
    if not project_exists(args.notifier_project):
        print(('Project {} not found. Please check if id is correct or if you '
               'have been granted access to it.'.format(args.notifier_project)))
        sys.exit(2)

def helpers_config(args):
    helpers.START_TIME = datetime.utcnow().strftime('%Y%m%d%H%M')
    helpers.DRY_RUN = args.dry_run
    helpers.BASE_DIR = os.path.join(os.path.dirname(
        os.path.abspath(inspect.stack()[0][1])), '..')


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    helpers_config(args)

    simulation_mode_disclaimer()

    validate_arguments(args)

    if args.use_dm:
        main_notifier(args)
    else:
        main_notifier_commands(args)
