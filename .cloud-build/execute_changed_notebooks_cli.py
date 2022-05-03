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

"""A CLI to process changed notebooks and execute them on Google Cloud Build"""

import argparse
import pathlib
import execute_changed_notebooks_helper


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("String value expected.")


parser = argparse.ArgumentParser(description="Run changed notebooks.")
parser.add_argument(
    "--test_paths_file",
    type=pathlib.Path,
    help="The path to the file that has newline-limited folders of notebooks that should be tested.",
    required=True,
)
parser.add_argument(
    "--base_branch",
    help="The base git branch to diff against to find changed files.",
    required=False,
)
parser.add_argument(
    "--container_uri",
    type=str,
    help="The container uri to run each notebook in.",
    required=True,
)
parser.add_argument(
    "--variable_project_id",
    type=str,
    help="The GCP project id. This is used to inject a variable value into the notebook before running.",
    required=True,
)
parser.add_argument(
    "--variable_region",
    type=str,
    help="The GCP region. This is used to inject a variable value into the notebook before running.",
    required=True,
)
parser.add_argument(
    "--staging_bucket",
    type=str,
    help="The GCS bucket for staging temporary files.",
    required=True,
)
parser.add_argument(
    "--artifacts_bucket",
    type=str,
    help="The GCP directory for storing executed notebooks.",
    required=True,
)
parser.add_argument(
    "--should_parallelize",
    type=str2bool,
    nargs="?",
    const=True,
    default=True,
    help="Should run notebooks in parallel.",
)

args = parser.parse_args()

notebooks = execute_changed_notebooks_helper.get_changed_notebooks(
    test_paths_file=args.test_paths_file,
    base_branch=args.base_branch,
)

execute_changed_notebooks_helper.process_and_execute_notebooks(
    notebooks=notebooks,
    container_uri=args.container_uri,
    staging_bucket=args.staging_bucket,
    artifacts_bucket=args.artifacts_bucket,
    variable_project_id=args.variable_project_id,
    variable_region=args.variable_region,
    should_parallelize=args.should_parallelize,
)
