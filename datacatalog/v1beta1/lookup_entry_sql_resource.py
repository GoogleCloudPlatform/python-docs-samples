# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-datacatalog

# sample-metadata
#   title:
#   description: Lookup Entry using SQL resource
#   usage: python3 samples/v1beta1/datacatalog_lookup_entry_sql_resource.py [--sql_name "[SQL Resource Name]"]


def sample_lookup_entry(sql_name: str):
    # [START data_catalog_lookup_entry_sql_resource_v1beta1]
    from google.cloud import datacatalog_v1beta1

    """
    Lookup Entry using SQL resource

    Args:
      sql_name (str): The SQL name of the Google Cloud Platform resource the Data Catalog
      entry represents.
      Examples:
      bigquery.table.`bigquery-public-data`.new_york_taxi_trips.taxi_zone_geom
      pubsub.topic.`pubsub-public-data`.`taxirides-realtime`
    """

    client = datacatalog_v1beta1.DataCatalogClient()

    # sql_name = '[SQL Resource Name]'
    entry = client.lookup_entry(request={"sql_resource": sql_name})
    print(f"Entry name: {entry.name}")
    print(f"Entry type: {datacatalog_v1beta1.EntryType(entry.type_).name}")
    print(f"Linked resource: {entry.linked_resource}")
    # [END data_catalog_lookup_entry_sql_resource_v1beta1]
    return entry


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--sql_name", type=str, default="[SQL Resource Name]")
    args = parser.parse_args()

    sample_lookup_entry(args.sql_name)


if __name__ == "__main__":
    main()
