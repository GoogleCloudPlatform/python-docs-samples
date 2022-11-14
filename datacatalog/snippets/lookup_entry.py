#!/usr/bin/env python

# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def lookup_entry(override_values):
    """Retrieves Data Catalog entry for the given Google Cloud Platform resource."""
    # [START data_catalog_lookup_dataset]
    # [START data_catalog_lookup_entry]
    from google.cloud import datacatalog_v1

    datacatalog = datacatalog_v1.DataCatalogClient()

    bigquery_project_id = "my_bigquery_project"
    dataset_id = "my_dataset"
    table_id = "my_table"
    pubsub_project_id = "my_pubsub_project"
    topic_id = "my_topic"

    # [END data_catalog_lookup_entry]

    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    bigquery_project_id = override_values.get(
        "bigquery_project_id", bigquery_project_id
    )
    dataset_id = override_values.get("dataset_id", dataset_id)
    table_id = override_values.get("table_id", table_id)
    pubsub_project_id = override_values.get("pubsub_project_id", pubsub_project_id)
    topic_id = override_values.get("topic_id", topic_id)

    # [START data_catalog_lookup_entry]
    # BigQuery Dataset via linked_resource
    resource_name = f"//bigquery.googleapis.com/projects/{bigquery_project_id}/datasets/{dataset_id}"

    entry = datacatalog.lookup_entry(request={"linked_resource": resource_name})
    print(
        f"Retrieved entry {entry.name} for BigQuery Dataset resource {entry.linked_resource}"
    )

    # BigQuery Dataset via sql_resource
    sql_resource = f"bigquery.dataset.`{bigquery_project_id}`.`{dataset_id}`"

    entry = datacatalog.lookup_entry(request={"sql_resource": sql_resource})
    print(
        f"Retrieved entry {entry.name} for BigQuery Dataset resource {entry.linked_resource}"
    )

    # BigQuery Table via linked_resource
    resource_name = (
        f"//bigquery.googleapis.com/projects/{bigquery_project_id}/datasets/{dataset_id}"
        f"/tables/{table_id}"
    )

    entry = datacatalog.lookup_entry(request={"linked_resource": resource_name})
    print(f"Retrieved entry {entry.name} for BigQuery Table {entry.linked_resource}")

    # BigQuery Table via sql_resource
    sql_resource = f"bigquery.table.`{bigquery_project_id}`.`{dataset_id}`.`{table_id}`"

    entry = datacatalog.lookup_entry(request={"sql_resource": sql_resource})
    print(
        f"Retrieved entry {entry.name} for BigQuery Table resource {entry.linked_resource}"
    )

    # Pub/Sub Topic via linked_resource
    resource_name = (
        f"//pubsub.googleapis.com/projects/{pubsub_project_id}/topics/{topic_id}"
    )

    entry = datacatalog.lookup_entry(request={"linked_resource": resource_name})
    print(
        f"Retrieved entry {entry.name} for Pub/Sub Topic resource {entry.linked_resource}"
    )

    # Pub/Sub Topic via sql_resource
    sql_resource = f"pubsub.topic.`{pubsub_project_id}`.`{topic_id}`"

    entry = datacatalog.lookup_entry(request={"sql_resource": sql_resource})
    print(
        f"Retrieved entry {entry.name} for Pub/Sub Topic resource {entry.linked_resource}"
    )
    # [END data_catalog_lookup_entry]
    # [END data_catalog_lookup_dataset]
