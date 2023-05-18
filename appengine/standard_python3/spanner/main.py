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

# [START gae_python38_cloud_spanner]
# [START gae_python3_cloud_spanner]
import os

from flask import Flask
from google.cloud import spanner

app = Flask(__name__)
spanner_client = spanner.Client()

instance_id = os.environ.get('SPANNER_INSTANCE')
database_id = os.environ.get('SPANNER_DATABASE')


@app.route('/')
def main():
    database = spanner_client.instance(instance_id).database(database_id)
    with database.snapshot() as snapshot:
        cursor = snapshot.execute_sql('SELECT 1')
    results = list(cursor)

    return f'Query Result: {results[0][0]}'
# [END gae_python3_cloud_spanner]
# [END gae_python38_cloud_spanner]
