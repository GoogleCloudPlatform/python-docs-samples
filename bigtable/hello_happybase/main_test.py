# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import random

from main import main

PROJECT = os.environ['GCLOUD_PROJECT']
BIGTABLE_CLUSTER = os.environ['BIGTABLE_CLUSTER']
TABLE_NAME_FORMAT = 'hello_happybase-system-tests-{}'
TABLE_NAME_RANGE = 10000


def test_main(capsys):
    table_name = TABLE_NAME_FORMAT.format(
        random.randrange(TABLE_NAME_RANGE))
    main(
        PROJECT,
        BIGTABLE_CLUSTER,
        table_name)

    out, _ = capsys.readouterr()
    if 'Creating the {} table.'.format(table_name) not in out:
        raise AssertionError
    if 'Writing some greetings to the table.' not in out:
        raise AssertionError
    if 'Getting a single greeting by row key.' not in out:
        raise AssertionError
    if 'Hello World!' not in out:
        raise AssertionError
    if 'Scanning for all greetings' not in out:
        raise AssertionError
    if 'Hello Cloud Bigtable!' not in out:
        raise AssertionError
    if 'Deleting the {} table.'.format(table_name) not in out:
        raise AssertionError
