# Copyright 2018 Google LLC
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

# [START gae_python37_cloudsql_mysql_pooling]
import os

from flask import Flask
import mysql.connector.pooling

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

# When deployed to App Engine, the `GAE_ENV` environment variable will be
# set to `standard`
if os.environ.get('GAE_ENV'):
    # If deployed, use the local socket interface for accessing Cloud SQL
    host = f'/cloudsql/{db_connection_name}'
else:
    # If running locally, use the TCP connections instead
    # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
    # so that your application can use 127.0.0.1:3306 to connect to your
    # Cloud SQL instance
    host = '127.0.0.1'

db_config = {
    'user': db_user,
    'password': db_password,
    'database': db_name,
    'host': host
}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name='cnxpool',
                                                      pool_size=3, **db_config)

app = Flask(__name__)


@app.route('/')
def main():
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    cursor.execute('SELECT NOW() as now;')
    result = cursor.fetchall()
    current_time = result[0][0]
    cursor.close()
    # If the connection comes from a pool, close() will send the connection
    # back to the pool instead of closing it
    cnx.close()

    return str(current_time)
# [END gae_python37_cloudsql_mysql_pooling]


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
