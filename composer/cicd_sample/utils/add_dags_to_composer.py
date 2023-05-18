# Copyright 2021 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START composer_cicd_add_dags_to_composer_utility]
from __future__ import annotations

import argparse
import glob
import os
from shutil import copytree, ignore_patterns
import tempfile

# Imports the Google Cloud client library
from google.cloud import storage


def _create_dags_list(dags_directory: str) -> tuple[str, list[str]]:
    temp_dir = tempfile.mkdtemp()

    # ignore non-DAG Python files
    files_to_ignore = ignore_patterns("__init__.py", "*_test.py")

    # Copy everything but the ignored files to a temp directory
    copytree(dags_directory, f"{temp_dir}/", ignore=files_to_ignore, dirs_exist_ok=True)

    # The only Python files left in our temp directory are DAG files
    # so we can exclude all non Python files
    dags = glob.glob(f"{temp_dir}/*.py")
    return (temp_dir, dags)


def upload_dags_to_composer(
    dags_directory: str, bucket_name: str, name_replacement: str = "dags/"
) -> None:
    """
    Given a directory, this function moves all DAG files from that directory
    to a temporary directory, then uploads all contents of the temporary directory
    to a given cloud storage bucket
    Args:
        dags_directory (str): a fully qualified path to a directory that contains a "dags/" subdirectory
        bucket_name (str): the GCS bucket of the Cloud Composer environment to upload DAGs to
        name_replacement (str, optional): the name of the "dags/" subdirectory that will be used when constructing the temporary directory path name Defaults to "dags/".
    """
    temp_dir, dags = _create_dags_list(dags_directory)

    if len(dags) > 0:
        # Note - the GCS client library does not currently support batch requests on uploads
        # if you have a large number of files, consider using
        # the Python subprocess module to run gsutil -m cp -r on your dags
        # See https://cloud.google.com/storage/docs/gsutil/commands/cp for more info
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        for dag in dags:
            # Remove path to temp dir
            dag = dag.replace(f"{temp_dir}/", name_replacement)

            try:
                # Upload to your bucket
                blob = bucket.blob(dag)
                blob.upload_from_filename(dag)
                print(f"File {dag} uploaded to {bucket_name}/{dag}.")
            except FileNotFoundError:
                current_directory = os.listdir()
                print(
                    f"{name_replacement} directory not found in {current_directory}, you may need to override the default value of name_replacement to point to a relative directory"
                )
                raise

    else:
        print("No DAGs to upload.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--dags_directory",
        help="Relative path to the source directory containing your DAGs",
    )
    parser.add_argument(
        "--dags_bucket",
        help="Name of the DAGs bucket of your Composer environment without the gs:// prefix",
    )

    args = parser.parse_args()

    upload_dags_to_composer(args.dags_directory, args.dags_bucket)
# [END composer_cicd_add_dags_to_composer_utility]
