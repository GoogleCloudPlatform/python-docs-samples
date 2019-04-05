#!/usr/bin/env python3

import argparse
import zipfile
import tempfile
import os
import helpers
import inspect
import fileinput
import sys
from shutil import copy2, SameFileError
from base import run_command
from commands import (
    choose_translation_mapper,
    get_properties_from_mapper,
    update_mapper_file_org_id
)


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

    parser_local.add_argument('-l',
                              '--local_zip_path',
                              help='Local Zip Path',
                              dest='local_zip_path')

    parser_local.add_argument('-sa',
                              '--sa_file',
                              help='Service account file full path.',
                              dest='sa_file')

    parser_local.set_defaults(dry_run=True)
    parser_local.set_defaults(local_zip_path=tempfile.gettempdir())

    return parser_local


def zip_and_store_cf(function_name, zip_name, bucket, local_zip_path=None, translation_sa=None):
    """ZIP cloud function files and update on bucket"""
    if translation_sa:
        sa_dir = os.path.join(
            helpers.BASE_DIR,
            'connector',
            'dm',
            'function',
            'translation',
            'accounts'
        )
        if not os.path.exists(sa_dir):
            os.makedirs(sa_dir)
        dest = os.path.join(sa_dir, 'cscc_api_client.json')
        print('Copying service account "{}" to "{}"'.format(translation_sa, dest))
        try:
            copy2(translation_sa, dest)
        except SameFileError:
            print('The service account passed already exists on translation.')
    zip_path = os.path.join(local_zip_path or tempfile.gettempdir(), zip_name)
    zip_file = zipfile.ZipFile(
        zip_path, mode='w', compression=zipfile.ZIP_DEFLATED)
    function_path = os.path.join(
        helpers.BASE_DIR, 'connector', 'dm', 'function', function_name)
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

    zip_and_store_cf(function_name, zip_name, bucket,
                     args.local_zip_path, args.sa_file)

    cmd = [
        'gcloud', 'beta', 'functions', 'deploy', function_name,
        '--source', bucket + '/' + zip_name,
        '--runtime', 'nodejs6',
        '--project', args.project_id
    ]
    run_command(cmd)
    print('Cloud function {} deployed'.format(function_name))


def helpers_config(args):
    helpers.DRY_RUN = args.dry_run
    helpers.BASE_DIR = os.path.join(os.path.dirname(
        os.path.abspath(inspect.stack()[0][1])), '..')
    sa_file = args.sa_file
    if sa_file and not os.path.isfile(sa_file):
        print('The service account file path passed is not valid: "{}".'.format(sa_file))
        sys.exit(1)


def get_organization_id():
    while True:
        ans = input(
            'Please enter the organization id (optional. No value will use the one set at partner mapping): ')
        if not ans:
            break
        if ans.isdigit():
            return ans


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    helpers_config(args)
    if args.cloud_function == 'translation':
        org_id = get_organization_id()
        mapper_file = choose_translation_mapper()
        if (org_id):
            update_mapper_file_org_id(org_id, mapper_file)
    if args.cloud_function == 'cleanup':
        org_id = get_organization_id()
        properties = get_properties_from_mapper(['org_name', 'service_path'])
        properties['org_name'] = 'organizations/{}'.format(org_id) if org_id else properties['org_name']

        CURRENT_FILE_DIR = os.path.split(os.path.abspath(__file__))[0]
        index_path = os.path.join(CURRENT_FILE_DIR, '../connector/dm/function/cleanup', 'index.js')
        text_to_search = "const orgName = null, servicePath = null;"
        text_to_replace = "const orgName = '" + properties['org_name'] + "', servicePath = '" + properties['service_path'] + "';"
        with fileinput.FileInput(index_path, inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace(text_to_search, text_to_replace), end='')
    update_cf(args)
