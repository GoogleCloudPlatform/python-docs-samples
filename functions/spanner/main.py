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

# [START spanner_functions_quickstart]
import functions_framework
from google.cloud import spanner

instance_id = "test-instance"
database_id = "example-db"

client = spanner.Client()
instance = client.instance(instance_id)
database = instance.database(database_id)


@functions_framework.http
def spanner_read_data(request):
    query = "SELECT * FROM Albums"

    outputs = []
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(query)

        for row in results:
            output = "SingerId: {}, AlbumId: {}, AlbumTitle: {}".format(*row)
            outputs.append(output)

    return "\n".join(outputs)


# [END spanner_functions_quickstart]
