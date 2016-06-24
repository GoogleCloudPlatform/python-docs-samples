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

import random
import re
import sys

from main import main

import pytest

TABLE_NAME_FORMAT = 'Hello-Bigtable-{}'
TABLE_NAME_RANGE = 10000


@pytest.mark.skipif(
    sys.version_info >= (3, 0),
    reason=("grpc doesn't yet support python3 "
            'https://github.com/grpc/grpc/issues/282'))
def test_main(cloud_config, capsys):
    table_name = TABLE_NAME_FORMAT.format(
        random.randrange(TABLE_NAME_RANGE))
    main(
        cloud_config.project,
        cloud_config.bigtable_cluster,
        cloud_config.bigtable_zone,
        table_name)

    out, _ = capsys.readouterr()
    assert re.search(
        re.compile(r'Creating the Hello-Bigtable-[0-9]+ table\.'), out)
    assert re.search(re.compile(r'Writing some greetings to the table\.'), out)
    assert re.search(re.compile(r'Getting a single greeting by row key.'), out)
    assert re.search(re.compile(r'greeting0: Hello World!'), out)
    assert re.search(re.compile(r'Scanning for all greetings'), out)
    assert re.search(re.compile(r'greeting1: Hello Cloud Bigtable!'), out)
    assert re.search(
        re.compile(r'Deleting the Hello-Bigtable-[0-9]+ table\.'), out)
