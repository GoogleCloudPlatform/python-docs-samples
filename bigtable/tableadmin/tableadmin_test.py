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
    assert 'Creating the {} table.'.format(table_name) in out
    assert 'Listing tables in current project.' in out
    assert 'Creating column family cf1 with with MaxAge GC Rule' in out
    assert 'Created MaxAge GC rule.' in out
    assert 'Created column family cf1 with MaxAge GC Rule.' in out
    assert 'Created Max Versions GC Rule.' in out
    assert 'Created column family cf2 with Max Versions GC Rule.' in out
    assert 'Created Union GC Rule.' in out
    assert 'Created column family cf3 with Union GC rule' in out
    assert 'Created Intersection GC Rule.' in out
    assert 'Created column family cf4 with Intersection GC rule.' in out
    assert 'Created Nested GC Rule.' in out
    assert 'Created column family cf5 with a Nested GC rule.' in out
    assert 'Printing Column Family and GC Rule for all column families.' in out
    assert 'Updating column family cf1 GC rule...' in out
    assert 'Updated column family cf1 GC rule' in out
    assert 'Print updated column family cf1 GC rule...' in out
    assert 'Column Family: cf1' in out
    assert 'max_num_versions: 1' in out
    assert 'Delete a column family cf2...' in out
    assert 'Column family cf2 deleted successfully.' in out


def test_delete_table(capsys):
    table_name = TABLE_NAME_FORMAT.format(
        random.randrange(TABLE_NAME_RANGE))

    delete_table(PROJECT, BIGTABLE_CLUSTER, table_name)
    out, _ = capsys.readouterr()

    assert 'Table {} exists.'.format(table_name) in out
    assert 'Deleting {} table.'.format(table_name) in out
    assert 'Deleted {} table.'.format(table_name) in out
