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

# [START firestore_count_query]
from google.cloud import firestore
from google.cloud.firestore_v1 import aggregation

"""
Creates an aggregate query (COUNT) that returns the number of results in the query.

See https://cloud.google.com/python/docs/reference/firestore/latest before running this sample.
"""


def create_count_query(project_id: str) -> None:
    """Builds an aggregate query that returns the number of results in the query.

    Arguments:
      project_id: your Google Cloud Project ID
    """
    client = firestore.Client(project=project_id)

    collection_ref = client.collection("users")
    query = collection_ref.where("born", ">", 1800)
    aggregate_query = aggregation.AggregationQuery(query)

    # `alias` to provides a key for accessing the aggregate query results
    aggregate_query.count(alias="all")

    results = aggregate_query.get()
    for result in results:
        print(f"Alias of results from query: {result[0].alias}")
        print(f"Number of results from query: {result[0].value}")


# [END firestore_count_query]
