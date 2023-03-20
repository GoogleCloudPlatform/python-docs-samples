# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START datastore_query_filter_or]
from google.cloud import datastore
from google.cloud.datastore import query

def query_filter_or(project_id: str) -> None:

    client = datastore.Client(project=project_id)

    or_query = client.query(kind="Task")
    or_filter = query.Or([
        query.PropertyFilter("description", "=", "Buy milk"),
        query.PropertyFilter("description", "=", "Feed cats"),
    ])

    or_query.add_filter(filter=or_filter)

    results = or_query.fetch()
    for result in results:
        print(result["description"])
# [END datastore_query_filter_or]
