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

"""
Samples for multi-inequality queries

See https://cloud.google.com/python/docs/reference/datastore/latest before running code.
"""


def query_filter_compound_multi_ineq():
    from google.cloud import datastore
    from google.cloud.datastore.query import PropertyFilter

    client = datastore.Client()
    # [START datastore_query_filter_compound_multi_ineq]
    query = client.query(kind="Task")
    query.add_filter(filter=PropertyFilter("priority", ">", 4))
    query.add_filter(filter=PropertyFilter("days", "<", 3))
    # [END datastore_query_filter_compound_multi_ineq]
    return query


def query_indexing_considerations():
    from google.cloud import datastore
    from google.cloud.datastore.query import PropertyFilter

    client = datastore.Client()
    # [START datastore_query_indexing_considerations]
    query = client.query(kind="employees")
    query.add_filter(filter=PropertyFilter("salary", ">", 100_000))
    query.add_filter(filter=PropertyFilter("experience", ">", 0))
    query.order = ["-salary", "-experience"]
    # [END datastore_query_indexing_considerations]
    return query


def query_order_fields():
    from google.cloud import datastore
    from google.cloud.datastore.query import PropertyFilter

    client = datastore.Client()
    # [START datastore_query_order_fields]
    query = client.query(kind="employees")
    query.add_filter(filter=PropertyFilter("salary", ">", 100_000))
    query.order = ["salary"]
    results = query.fetch()
    # Order results by `experience`
    sorted_results = sorted(results, key=lambda x: x.get("experience"))
    # [END datastore_query_order_fields]
    return sorted_results
