#!/usr/bin/env python3

import argparse
import inspect
from datetime import datetime
import os
import sys
import logger

import helpers
from base import run_command, scape_to_os
from commands import (
    project_exists,
    use_service_account,
    topic_exists,
    has_file,
    bucket_status,
    deployment_exists,
    use_service_account_disclaimer,
    simulation_mode_disclaimer,
    validate_key_file
)

from update_cloud_function import zip_and_store_cf


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

    # TODO: Remove or make optional the use of a service account (akieras/dandrade).
    # (this was commented out to simplify the installation process)
    # parser_local.add_argument('-k',
    #                           '--key_file',
    #                           help='Service Account Key File',
    #                           dest='key_file',
    #                           required=True)

    parser_local.add_argument('-o',
                              '--organization_id',
                              help='Organization ID',
                              dest='organization_id',
                              required=True)

    parser_local.add_argument('-p',
                              '--project',
                              help='Project name',
                              dest='project',
                              required=True)

    parser_local.add_argument('-r',
                              '--region',
                              help='Region',
                              dest='region',
                              required=True)

    parser_local.add_argument('-cb',
                              '--cf_bucket',
                              help='Cloud function bucket',
                              dest='cf_bucket_name')

    parser_local.add_argument('-ak',
                              '--api_key',
                              help='SCC api key',
                              dest='api_key',
                              required=True)

    parser_local.add_argument('-dm',
                              '--use_dm',
                              help='Use Deployment Manager for the installation process',
                              dest='use_dm',
                              action='store_true')

    parser_local.set_defaults(dry_run=True)

    return parser_local


def validate_arguments(args):
    if not project_exists(args.project):
        print(('Project {} not found. Please check if id is correct or if you '
               'have been granted access to it.'.format(args.project)))
        sys.exit(2)

    cscc_api_client_file = os.path.join(
        helpers.BASE_DIR,
        'function', 'transformer', 'accounts', 'cscc_api_client.json'
    )
    if not has_file(cscc_api_client_file):
        print('CSCC api client file does not exist.\nPlease place a valid file '
              'at {}'.format(cscc_api_client_file))
        sys.exit(4)


def helpers_config(args):
    helpers.START_TIME = datetime.utcnow().strftime('%Y%m%d%H%M')
    helpers.DRY_RUN = args.dry_run
    helpers.BASE_DIR = os.path.join(os.path.dirname(
        os.path.abspath(inspect.stack()[0][1])), '..')


def main_setup(args):
    project = args.project
    # Project
    print('project validation')
    if not project_exists(project):
        print('The project_id passed does not exists')
        sys.exit(4)
    apis_dm_name = '-'.join(['apis', args.project])
    if not deployment_exists(project, apis_dm_name):
        apis_template = os.path.join(helpers.BASE_DIR, 'dm', 'apis.py')
        cmd = [
            'gcloud', 'deployment-manager', 'deployments', 'create',
            apis_dm_name,
            '--template', apis_template,
            '--properties',
            ",".join([
                'concurrent_api_activation:' + str(False)
            ]),
            '--project', project
        ]
        run_command(cmd)
    # CF Bucket
    cf_bucket_name = args.cf_bucket_name or 'bucket-cf-' + args.project
    print('cloud function bucket creation.')
    cf_bucket_status = bucket_status(cf_bucket_name)
    if 'NotFound' == cf_bucket_status:
        bucket_template = os.path.join(
            helpers.BASE_DIR, 'dm', 'bucket.py')
        cmd = [
            'gcloud', 'deployment-manager', 'deployments', 'create',
            '-'.join(['bucket', project,
                      datetime.utcnow().strftime('%Y%m%d%H%M%S')]),
            '--template', bucket_template,
            '--properties',
            ",".join([
                'region:' + scape_to_os(args.region),
                'bucketname:' + cf_bucket_name,
            ]),
            '--project', project
        ]
        run_command(cmd)
    # Application (cloud functions and topics)
    print('application creation.')
    infra_dm_name = '-'.join(['infra', args.project])
    if not deployment_exists(project, infra_dm_name):
        zip_and_store_cf('transformer',
                         'transformer.zip', 'gs://' + cf_bucket_name,
                         args.organization_id,
                         args.api_key)
        zip_and_store_cf('logger', 'logger.zip',
                         'gs://' + cf_bucket_name,
                         args.organization_id,
                         args.api_key)

        infra_template = os.path.join(
            helpers.BASE_DIR, 'dm', 'infra.py')
        cmd = [
            'gcloud', 'deployment-manager', 'deployments', 'create',
            infra_dm_name,
            '--template', infra_template,
            '--properties',
            ",".join([
                'region:' + scape_to_os(args.region),
                'cfbucket:' + cf_bucket_name,
            ]),
            '--project', project
        ]
        run_command(cmd)


def main_setup_commands(args):
    # project
    project = args.project

    # bucket
    logger.step('Creating buckets to store cloud functions...')
    cf_bucket_name = args.cf_bucket_name or 'bucket-cf-' + args.project
    cf_bucket_status = bucket_status(cf_bucket_name)
    if cf_bucket_status == 'NotFound':
        logger.info('Bucket not found, creating...')
        cmd = [
            'gsutil', 'mb',
            '-p', project,
            '-c', 'REGIONAL',
            '-l', args.region,
            'gs://{}/'.format(cf_bucket_name)
        ]
        run_command(cmd)
    else:
        logger.warn('Bucket already exists, skipping creation')

    # pub/sub
    logger.step('Creating Pub/Sub topic...')
    if not topic_exists(project, 'entrypoint'):
        logger.info('Creating entrypoint topic')
        cmd = [
            'gcloud', 'pubsub', 'topics', 'create',
            'entrypoint',
            '--project', project
        ]
        run_command(cmd)
    else:
        logger.warn('entrypoint topic already exists, skipping creation')

    if not topic_exists(project, 'redirect'):
        logger.info('Creating redirect topic')
        cmd = [
            'gcloud', 'pubsub', 'topics', 'create',
            'redirect',
            '--project', project
        ]
        run_command(cmd)
    else:
        logger.warn('redirect topic already exists, skipping creation')

    # cloud functions
    logger.step('Deploying Cloud Function...')
    logger.info('Creating zip and uploading transformer function...')
    zip_and_store_cf('transformer', 'transformer.zip', 'gs://{}'.format(cf_bucket_name), args.organization_id, args.api_key)
    logger.info('Deploying transformer Cloud Function...')
    cmd = [
        'gcloud', 'functions', 'deploy', 'transformer',
        '--project', project,
        '--source', 'gs://{}/{}.zip'.format(cf_bucket_name, 'transformer'),
        '--entry-point', 'transform',
        '--trigger-topic', 'entrypoint',
        '--region', args.region,
        '--timeout', '180',
        '--runtime', 'nodejs6',
        '--retry'
    ]
    run_command(cmd)

    logger.info('Creating zip and uploading logger function...')
    zip_and_store_cf('logger', 'logger.zip', 'gs://{}'.format(cf_bucket_name), args.organization_id, args.api_key)
    logger.info('Deploying logger Cloud Function...')
    cmd = [
        'gcloud', 'functions', 'deploy', 'logger',
        '--project', project,
        '--source', 'gs://{}/{}.zip'.format(cf_bucket_name, 'logger'),
        '--entry-point', 'log',
        '--trigger-topic', 'redirect',
        '--region', args.region,
        '--timeout', '180',
        '--runtime', 'nodejs6',
        '--retry'
    ]
    run_command(cmd)


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    helpers_config(args)

    simulation_mode_disclaimer()

    # TODO: Remove or make optional the use of a service account (akieras/dandrade).
    # (this was commented out to simplify the installation process)
    # validate_key_file(args.key_file)

    # use_service_account(args.key_file)

    validate_arguments(args)

    if args.use_dm:
        main_setup(args)
    else:
        main_setup_commands(args)
