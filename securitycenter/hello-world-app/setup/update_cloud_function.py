#!/usr/bin/env python3

import argparse
import inspect
import os
import tempfile
import zipfile

import helpers
from base import run_command


def create_parser():
    """CLI parser."""
    parser_local = argparse.ArgumentParser(
        description='Update cloud function of a project.')

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

    parser_local.add_argument('-p',
                              '--project_id',
                              help='Project ID',
                              dest='project_id',
                              required=True)

    parser_local.add_argument('-b',
                              '--bucket_name',
                              help='bucket name',
                              dest='bucket_name',
                              required=True)

    parser_local.add_argument('-cf',
                              '--cloud_function',
                              help='Cloud function to update',
                              dest='cloud_function',
                              required=True)

    parser_local.add_argument('-ak',
                              '--api_key',
                              help='SCC api key',
                              dest='api_key',
                              required=True)

    parser_local.set_defaults(dry_run=True)

    return parser_local


def update_transform_config(organization_id, api_key):
    """Update the organization id and api key on config.json from transform cloud function"""
    with open(os.path.join(
            helpers.BASE_DIR, 'function', 'transformer', 'config.json'), 'w') as f:
        f.write('{{"ORG_ID" : "{}", "API_KEY" : "{}"}}'
                .format(organization_id, api_key))


def zip_and_store_cf(function_name, zip_name, bucket, organization_id, api_key):
    """ZIP cloud function files and update on bucket"""
    update_transform_config(organization_id, api_key)
    zip_path = os.path.join(tempfile.gettempdir(), zip_name)
    zip_file = zipfile.ZipFile(
        zip_path, mode='w', compression=zipfile.ZIP_DEFLATED)
    function_path = os.path.join(
        helpers.BASE_DIR, 'function', function_name)
    for dirname, subdirs, files in os.walk(function_path):
        if 'node_modules' in subdirs:
            subdirs.remove('node_modules')
        for filename in files:
            zip_file.write(
                os.path.join(dirname, filename),
                os.path.join(dirname.replace(function_path, ''), filename))
    zip_file.close()
    print('ZIP file created: "{}"'.format(zip_path))

    cmd = [
        'gsutil', 'cp', zip_path, bucket
    ]
    run_command(cmd)
    print('ZIP uploaded on bucket: "{}"'.format(bucket))


def update_cf(args):
    """Update cloud function"""
    function_name = args.cloud_function
    zip_name = function_name + '.zip'
    bucket = 'gs://' + args.bucket_name

    zip_and_store_cf(
        function_name, zip_name, bucket, args.organization_id, args.api_key
    )

    cmd = [
        'gcloud', 'beta', 'functions', 'deploy', function_name,
        '--source', bucket + '/' + zip_name,
        '--runtime', 'nodejs6',
        '--project', args.project_id
    ]
    run_command(cmd)
    print('Clound function {} updated'.format(function_name))


def helpers_config(args):
    helpers.DRY_RUN = args.dry_run
    helpers.BASE_DIR = os.path.join(os.path.dirname(
        os.path.abspath(inspect.stack()[0][1])), '..')


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    helpers_config(args)
    update_cf(args)
