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


def query_or_filter(client) -> None:
    # [START firestore_query_filter_or]
    from google.cloud.firestore_v1.base_query import FieldFilter, Or

    col_ref = client.collection("cities")
    # Execute the query
    query = col_ref.where(
        filter=Or(
            [
                FieldFilter("capital", "==", True),
                FieldFilter("population", ">", 1_000_000),
            ]
        )
    )
    docs = query.stream()
    # [END firestore_query_filter_or]

    print("Documents found:")
    for doc in docs:
        print(f"ID: {doc.id}")


def query_or_compound_filter(client) -> None:
    # [START firestore_query_filter_or_compound]
    from google.cloud.firestore_v1.base_query import FieldFilter, Or, And

    col_ref = client.collection("cities")
    # Execute the query
    query = col_ref.where(
        filter=And(
            [
                FieldFilter("state", "==", "CA"),
                Or(
                    [
                        FieldFilter("capital", "==", True),
                        FieldFilter("population", ">", 1000000),
                    ]
                ),
            ]
        )
    )
    docs = query.stream()
    # [END firestore_query_filter_or_compound]

    print("Documents found:")
    for doc in docs:
        print(f"ID: {doc.id}")
