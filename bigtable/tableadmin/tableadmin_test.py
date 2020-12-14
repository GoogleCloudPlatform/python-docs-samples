#!/usr/bin/env python

# Copyright 2018, Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import random

from tableadmin import create_table
from tableadmin import delete_table
from tableadmin import run_table_operations

PROJECT = os.environ['GCLOUD_PROJECT']
BIGTABLE_CLUSTER = os.environ['BIGTABLE_CLUSTER']
TABLE_NAME_FORMAT = 'hello-bigtable-system-tests-{}'
TABLE_NAME_RANGE = 10000


def test_run_table_operations(capsys):
    table_name = TABLE_NAME_FORMAT.format(
        random.randrange(TABLE_NAME_RANGE))

    run_table_operations(PROJECT, BIGTABLE_CLUSTER, table_name)
    out, _ = capsys.readouterr()

    if 'Creating the ' + table_name + ' table.' not in out:
        raise AssertionError
    if 'Listing tables in current project.' not in out:
        raise AssertionError
    if 'Creating column family cf1 with with MaxAge GC Rule' not in out:
        raise AssertionError
    if 'Created column family cf1 with MaxAge GC Rule.' not in out:
        raise AssertionError
    if 'Created column family cf2 with Max Versions GC Rule.' not in out:
        raise AssertionError
    if 'Created column family cf3 with Union GC rule' not in out:
        raise AssertionError
    if 'Created column family cf4 with Intersection GC rule.' not in out:
        raise AssertionError
    if 'Created column family cf5 with a Nested GC rule.' not in out:
        raise AssertionError
    if 'Printing Column Family and GC Rule for all column families.' not in out:
        raise AssertionError
    if 'Updating column family cf1 GC rule...' not in out:
        raise AssertionError
    if 'Updated column family cf1 GC rule' not in out:
        raise AssertionError
    if 'Print column family cf1 GC rule after update...' not in out:
        raise AssertionError
    if 'Column Family: cf1' not in out:
        raise AssertionError
    if 'max_num_versions: 1' not in out:
        raise AssertionError
    if 'Delete a column family cf2...' not in out:
        raise AssertionError
    if 'Column family cf2 deleted successfully.' not in out:
        raise AssertionError


def test_delete_table(capsys):
    table_name = TABLE_NAME_FORMAT.format(
        random.randrange(TABLE_NAME_RANGE))
    create_table(PROJECT, BIGTABLE_CLUSTER, table_name)

    delete_table(PROJECT, BIGTABLE_CLUSTER, table_name)
    out, _ = capsys.readouterr()

    if 'Table ' + table_name + ' exists.' not in out:
        raise AssertionError
    if 'Deleting ' + table_name + ' table.' not in out:
        raise AssertionError
    if 'Deleted ' + table_name + ' table.' not in out:
        raise AssertionError
