# -*- coding: utf-8 -*-
#
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

# DO NOT EDIT! This is a generated sample ("Request",  "datacatalog_lookup_entry")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-datacatalog

# sample-metadata
#   title:
#   description: Lookup Entry
#   usage: python3 samples/v1beta1/datacatalog_lookup_entry.py [--resource_name "[Full Resource Name]"]

# [START datacatalog_lookup_entry]
from google.cloud import datacatalog_v1beta1
from google.cloud.datacatalog_v1beta1 import enums


def sample_lookup_entry(resource_name):
    """
    Lookup Entry

    Args:
      resource_name The full name of the Google Cloud Platform resource the Data
      Catalog entry represents.
      See: https://cloud.google.com/apis/design/resource_names#full_resource_name
      Examples:
      //bigquery.googleapis.com/projects/bigquery-public-data/datasets/new_york_taxi_trips/tables/taxi_zone_geom
      //pubsub.googleapis.com/projects/pubsub-public-data/topics/taxirides-realtime
    """

    client = datacatalog_v1beta1.DataCatalogClient()

    # resource_name = '[Full Resource Name]'
    response = client.lookup_entry(linked_resource=resource_name)
    entry = response
    print(u"Entry name: {}".format(entry.name))
    print(u"Entry type: {}".format(enums.EntryType(entry.type).name))
    print(u"Linked resource: {}".format(entry.linked_resource))


# [END datacatalog_lookup_entry]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--resource_name", type=str, default="[Full Resource Name]")
    args = parser.parse_args()

    sample_lookup_entry(args.resource_name)


if __name__ == "__main__":
    main()
