# Copyright 2021 Google Inc. All Rights Reserved.
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

import os
import re
import subprocess

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]


def test_create_bigquery_table():
    output = str(
        subprocess.check_output(
            'python setup/products_create_bigquery_table.py',
            shell=True))
    assert re.match(
        f'.*Creating dataset {project_id}.products.*', output)
    assert re.match(
        f'(.*dataset {project_id}.products already exists.*|.*dataset is created.*)', output)
    assert re.match(
        f'.*Creating BigQuery table {project_id}.products.products.*', output)
    assert re.match(
        f'(.*table {project_id}.products.products already exists.*|.*table is created.*)', output)
    assert re.match(
        f'.*Uploading data from ../resources/products.json to the table {project_id}.products.products.*', output)
    assert re.match(
        f'.*Creating BigQuery table {project_id}.products.products_some_invalid.*',
        output)
    assert re.match(
        f'(.*table {project_id}.products.products_some_invalid already exists.*|.*table is created.*)',
        output)
    assert re.match(
        f'.*Uploading data from ../resources/products_some_invalid.json to the table {project_id}.products.products_some_invalid.*',
        output)
