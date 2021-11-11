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
#   description: Lookup Entry
#   usage: python3 samples/v1beta1/datacatalog_lookup_entry.py [--resource_name "[Full Resource Name]"]


def sample_lookup_entry(resource_name: str):
    # [START data_catalog_lookup_entry_v1beta1]
    from google.cloud import datacatalog_v1beta1

    """
    Lookup Entry

    Args:
      resource_name (str): The full name of the Google Cloud Platform resource the Data
      Catalog entry represents.
      See: https://cloud.google.com/apis/design/resource_names#full_resource_name
      Examples:
      //bigquery.googleapis.com/projects/bigquery-public-data/datasets/new_york_taxi_trips/tables/taxi_zone_geom
      //pubsub.googleapis.com/projects/pubsub-public-data/topics/taxirides-realtime
    """

    client = datacatalog_v1beta1.DataCatalogClient()
    entry = client.lookup_entry(request={"linked_resource": resource_name})
    print(f"Entry name: {entry.name}")
    print(f"Entry type: {datacatalog_v1beta1.EntryType(entry.type_).name}")
    print(f"Linked resource: {entry.linked_resource}")
    # [END data_catalog_lookup_entry_v1beta1]
    return entry


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--resource_name", type_=str, default="[Full Resource Name]")
    args = parser.parse_args()

    sample_lookup_entry(args.resource_name)


if __name__ == "__main__":
    main()
