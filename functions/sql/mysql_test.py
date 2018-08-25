# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re

import mock

env_vars = {
  'SQL_USER': os.getenv('MYSQL_USER'),
  'SQL_PASSWORD': os.getenv('MYSQL_PASSWORD'),
  'SQL_NAME': os.getenv('MYSQL_NAME'),
  'INSTANCE_CONNECTION_NAME':
  os.getenv('INSTANCE_CONNECTION_PREFIX') + '-mysql'
}

date_regex = re.compile('\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}')


@mock.patch.dict(os.environ, env_vars)
def test_mysql():
    import mysql_sample
    results = mysql_sample.mysql_demo(None)
    assert date_regex.match(results)
