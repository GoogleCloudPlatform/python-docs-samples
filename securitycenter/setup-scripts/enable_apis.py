#!/usr/bin/env python3

import argparse
import inspect
import sys
import os
import json
from datetime import datetime

import helpers
from base import run_command, run_command_readonly
from commands import project_exists, simulation_mode_disclaimer


def create_parser():
    """CLI parser."""
    parser_local = argparse.ArgumentParser(
        description='Enable APIs for a type of project.')

    parser_local.add_argument('-c',
                              '--connector-apis',
                              help='Enable APIs for a connector project.',
                              dest='connector_apis',
                              action='store_true')

    parser_local.add_argument('-r',
                              '--creator-apis',
                              help='Enable APIs for a creator project.',
                              dest='creator_apis',
                              action='store_true')

    parser_local.add_argument('-n',
                              '--notifier-apis',
                              help='Enable APIs for a notifier project.',
                              dest='notifier_apis',
                              action='store_true')

    parser_local.add_argument('-qb',
                              '--query-builder-apis',
                              help='Enable APIs for a query builder project.',
                              dest='query_builder_apis',
                              action='store_true')

    parser_local.add_argument('-lg',
                              '--scc-logs-apis',
                              help='Enable APIs for a SCC Logs project.',
                              dest='scc_logs',
                              action='store_true')

    parser_local.add_argument('-d',
                              '--dns-apis',
                              help='Enable APIs for a dns project.',
                              dest='dns_apis',
                              action='store_true')

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

    parser_local.add_argument('-p',
                              '--project_id',
                              help='Project ID',
                              dest='project_id',
                              required=True)

    parser_local.set_defaults(dry_run=True)
    parser_local.set_defaults(connector_apis=False)
    parser_local.set_defaults(creator_apis=False)
    parser_local.set_defaults(notifier_apis=False)
    parser_local.set_defaults(query_builder_apis=False)
    parser_local.set_defaults(scc_logs=False)

    return parser_local


def validate_arguments(args):
    if not project_exists(args.project_id):
        print('project {} does not exist. Aborting script execution.'
              .format(args.project_id))
        sys.exit(1)


def get_enabled_apis_on_project(project_id):
    print('Getting enabled apis on project {}\n'.format(project_id))
    result_ = run_command_readonly([
        'gcloud', 'services', 'list',
        '--enabled',
        '--format="(NAME:format=json)"',
        '--project', project_id
    ])
    return json.loads(result_.decode("utf-8").strip())


def enable_services_on_project(project_id, apis):
    if not apis:
        print("There are no APIs to enable.")
        return

    enabled_apis = get_enabled_apis_on_project(project_id)
    apis_to_enable = [api for api in apis if api not in enabled_apis]
    if apis_to_enable:
        services = " ".join(apis_to_enable)
        print("Enabling {} on project {}\n".format(services, project_id))
        run_command([
            'gcloud', 'services', 'enable', services,
            '--project', project_id
        ])
    else:
        print("All needed APIs {} already enabled on project {}\n"
              .format(apis, project_id))


def enable_apis(project_id,
                connector_apis=False,
                creator_apis=False,
                notifier_apis=False,
                query_builder_apis=False,
                dns_apis=False,
                scc_logs=False):

    api_candidates = set()

    if connector_apis:
        api_candidates.update([
            'appengine.googleapis.com',
            'compute.googleapis.com',
            'deploymentmanager.googleapis.com',
            'cloudresourcemanager.googleapis.com',
            'storage-component.googleapis.com',
            'monitoring.googleapis.com',
            'logging.googleapis.com',
            'pubsub.googleapis.com',
            'datastore.googleapis.com',
            'cloudfunctions.googleapis.com',
            'cloudbuild.googleapis.com'
        ])

    if creator_apis:
        api_candidates.update([
            'appengine.googleapis.com',
            'compute.googleapis.com',
            'deploymentmanager.googleapis.com',
            'cloudresourcemanager.googleapis.com',
            'storage-component.googleapis.com',
            'monitoring.googleapis.com',
            'logging.googleapis.com',
            'pubsub.googleapis.com',
            'datastore.googleapis.com',
            'cloudbuild.googleapis.com',
            'securitycenter.googleapis.com'
        ])

    if notifier_apis:
        api_candidates.update([
            'servicemanagement.googleapis.com',
            'appengine.googleapis.com',
            'cloudbuild.googleapis.com',
            'cloudfunctions.googleapis.com',
            'cloudresourcemanager.googleapis.com',
            'compute.googleapis.com',
            'datastore.googleapis.com',
            'deploymentmanager.googleapis.com',
            'endpoints.googleapis.com',
            'logging.googleapis.com',
            'monitoring.googleapis.com',
            'pubsub.googleapis.com',
            'storage-component.googleapis.com'
        ])

    if query_builder_apis:
        api_candidates.update([
            'cloudapis.googleapis.com',
            'cloudbuild.googleapis.com',
            'clouddebugger.googleapis.com',
            'cloudtrace.googleapis.com',
            'compute.googleapis.com',
            'container.googleapis.com',
            'containerregistry.googleapis.com',
            'deploymentmanager.googleapis.com',
            'logging.googleapis.com',
            'monitoring.googleapis.com',
            'oslogin.googleapis.com',
            'replicapool.googleapis.com',
            'replicapoolupdater.googleapis.com',
            'resourceviews.googleapis.com',
            'servicemanagement.googleapis.com',
            'serviceusage.googleapis.com',
            'sourcerepo.googleapis.com',
            'sql-component.googleapis.com',
            'sqladmin.googleapis.com',
            'stackdriver.googleapis.com',
            'storage-api.googleapis.com',
            'pubsub.googleapis.com',
            'storage-component.googleapis.com',
            'securitycenter.googleapis.com',
            'iamcredentials.googleapis.com',
            'cloudresourcemanager.googleapis.com',
            'iam.googleapis.com'
        ])

    if dns_apis:
        api_candidates.update([
            'dns.googleapis.com',
            'compute.googleapis.com'
        ])

    if scc_logs:
        api_candidates.update([
            'cloudbuild.googleapis.com',
            'cloudfunctions.googleapis.com',
            'cloudresourcemanager.googleapis.com',
            'compute.googleapis.com',
            'datastore.googleapis.com',
            'logging.googleapis.com',
            'monitoring.googleapis.com',
            'pubsub.googleapis.com',
            'storage-component.googleapis.com',
            'dataflow.googleapis.com'
        ])

    enable_services_on_project(project_id, api_candidates)


def helpers_config(args):
    helpers.START_TIME = datetime.utcnow().strftime('%Y%m%d%H%M')
    helpers.DRY_RUN = args.dry_run
    helpers.BASE_DIR = os.path.join(os.path.dirname(
        os.path.abspath(inspect.stack()[0][1])), '..')


def run_steps(args):
    helpers_config(args)
    simulation_mode_disclaimer()
    enable_apis(args.project_id,
                args.connector_apis,
                args.creator_apis,
                args.notifier_apis,
                args.query_builder_apis,
                args.dns_apis,
                args.scc_logs)
    simulation_mode_disclaimer()


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    validate_arguments(args)
    run_steps(args)
