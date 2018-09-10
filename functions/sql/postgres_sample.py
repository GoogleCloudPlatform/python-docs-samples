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

# [START functions_sql_postgres]
from os import getenv

from psycopg2.pool import SimpleConnectionPool

is_production = getenv('SUPERVISOR_HOSTNAME') is not None

# TODO(developer): specify SQL connection details
pg_config = {
  'user': getenv('SQL_USER'),
  'password': getenv('SQL_PASSWORD'),
  'dbname': getenv('SQL_DATABASE'),
}

if is_production:
    pg_config['host'] = '/cloudsql/' + getenv('INSTANCE_CONNECTION_NAME')
else:
    pg_config['host'] = 'localhost'

pg_pool = SimpleConnectionPool(1, 1, **pg_config)


def postgres_demo(request):
    with pg_pool.getconn().cursor() as cursor:
        cursor.execute('SELECT NOW() as now')
        results = cursor.fetchone()
        return str(results[0])
# [END functions_sql_postgres]
