#!/usr/bin/env python3

import os
import tempfile
import zipfile

import helpers
from base import run_command


def zip_and_store_cf(function_name, zip_name, bucket):
    """ZIP cloud function files and update on bucket"""
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
