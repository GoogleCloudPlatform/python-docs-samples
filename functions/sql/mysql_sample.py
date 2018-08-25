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

# [START functions_sql_mysql]
from os import getenv

import pymysql

is_production = getenv('SUPERVISOR_HOSTNAME') is not None

# TODO(developer): specify SQL connection details
mysql_config = {
  'user': getenv('SQL_USER'),
  'password': getenv('SQL_PASSWORD'),
  'db': getenv('SQL_DATABASE'),
  'charset': 'utf8mb4',
  'cursorclass': pymysql.cursors.DictCursor,
  'autocommit': True
}

if is_production:
    mysql_config['unix_socket'] = \
      '/cloudsql/' + getenv('INSTANCE_CONNECTION_NAME')

# Create SQL connection globally to enable reuse
mysql_connection = pymysql.connect(**mysql_config)


def mysql_demo(request):
    with mysql_connection.cursor() as cursor:
        cursor.execute('SELECT NOW() as now')
        results = cursor.fetchone()
        return str(results['now'])
# [END functions_sql_mysql]
