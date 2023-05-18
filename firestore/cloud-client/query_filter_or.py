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

# [START firestore_query_filter_or]
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter, Or


def query_or_composite_filter(project_id: str) -> None:
    # Instantiate the Firestore client
    client = firestore.Client(project=project_id)
    col_ref = client.collection("users")

    filter_1 = FieldFilter("birthYear", "==", 1906)
    filter_2 = FieldFilter("birthYear", "==", 1912)

    # Create the union filter of the two filters (queries)
    or_filter = Or(filters=[filter_1, filter_2])

    # Execute the query
    docs = col_ref.where(filter=or_filter).stream()

    print("Documents found:")
    for doc in docs:
        print(f"ID: {doc.id}")
# [END firestore_query_filter_or]
