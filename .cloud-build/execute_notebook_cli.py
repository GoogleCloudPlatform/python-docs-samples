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

"""A CLI to download (optional) and run a single notebook locally"""

import argparse
import execute_notebook_helper

parser = argparse.ArgumentParser(description="Run a single notebook locally.")
parser.add_argument(
    "--notebook_source",
    type=str,
    help="Local filepath or GCS URI to notebook.",
    required=True,
)
parser.add_argument(
    "--output_file_or_uri",
    type=str,
    help="Local file or GCS URI to save executed notebook to.",
    required=True,
)

args = parser.parse_args()
execute_notebook_helper.execute_notebook(
    notebook_source=args.notebook_source,
    output_file_or_uri=args.output_file_or_uri,
    should_log_output=True,
)
