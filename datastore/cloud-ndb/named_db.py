# Copyright 2023 Google LLC
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


def create_named_db_client():
    # [START datastore_ndb_named_db]
    import os

    from google.cloud import ndb

    database = os.environ.get("DATASTORE_DATABASE", "prod-database")
    client = ndb.Client(database=database)
    # [END datastore_ndb_named_db]
    return client
