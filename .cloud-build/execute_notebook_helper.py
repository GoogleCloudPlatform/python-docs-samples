#!/usr/bin/env python
# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Methods to run a notebook locally"""

import sys
import os
import errno
import papermill as pm
import shutil

from utils import util
from google.cloud.aiplatform import utils

# This script is used to execute a notebook and write out the output notebook.


def execute_notebook(
    notebook_source: str,
    output_file_or_uri: str,
    should_log_output: bool,
):
    """Execute a single notebook using Papermill"""
    file_name = os.path.basename(os.path.normpath(notebook_source))

    # Download notebook if it's a GCS URI
    if notebook_source.startswith("gs://"):
        # Extract uri components
        bucket_name, prefix = utils.extract_bucket_and_prefix_from_gcs_path(
            notebook_source
        )

        # Download remote notebook to local file system
        notebook_source = file_name
        util.download_file(
            bucket_name=bucket_name, blob_name=prefix, destination_file=notebook_source
        )

    execution_exception = None

    # Execute notebook
    try:
        # Execute notebook
        pm.execute_notebook(
            input_path=notebook_source,
            output_path=notebook_source,
            progress_bar=should_log_output,
            request_save_on_cell_execute=should_log_output,
            log_output=should_log_output,
            stdout_file=sys.stdout if should_log_output else None,
            stderr_file=sys.stderr if should_log_output else None,
        )
    except Exception as exception:
        execution_exception = exception
    finally:
        # Copy executed notebook
        if output_file_or_uri.startswith("gs://"):
            # Upload to GCS path
            util.upload_file(notebook_source, remote_file_path=output_file_or_uri)

            print("\n=== EXECUTION FINISHED ===\n")
            print(
                f"Please debug the executed notebook by downloading: {output_file_or_uri}"
            )
            print("\n======\n")
        else:
            # Create directories if they don't exist
            if not os.path.exists(os.path.dirname(output_file_or_uri)):
                try:
                    os.makedirs(os.path.dirname(output_file_or_uri))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            print(f"Writing output to: {output_file_or_uri}")
            shutil.move(notebook_source, output_file_or_uri)

        if execution_exception:
            raise execution_exception
