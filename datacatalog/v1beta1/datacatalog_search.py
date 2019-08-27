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

# DO NOT EDIT! This is a generated sample ("RequestPagedAll",  "datacatalog_search")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-datacatalog

# sample-metadata
#   title:
#   description: Search Catalog
#   usage: python3 samples/v1beta1/datacatalog_search.py [--include_project_id "[Google Cloud Project ID]"] [--include_gcp_public_datasets false] [--query "[String in search query syntax]"]

# [START datacatalog_search]
from google.cloud import datacatalog_v1beta1
from google.cloud.datacatalog_v1beta1 import enums


def sample_search_catalog(include_project_id, include_gcp_public_datasets, query):
    """
    Search Catalog

    Args:
      include_project_id Your Google Cloud project ID.
      include_gcp_public_datasets If true, include Google Cloud Platform (GCP) public
      datasets in the search results.
      query Your query string.
      See: https://cloud.google.com/data-catalog/docs/how-to/search-reference
      Example: system=bigquery type=dataset
    """

    client = datacatalog_v1beta1.DataCatalogClient()

    # include_project_id = '[Google Cloud Project ID]'
    # include_gcp_public_datasets = False
    # query = '[String in search query syntax]'
    include_project_ids = [include_project_id]
    scope = {
        "include_project_ids": include_project_ids,
        "include_gcp_public_datasets": include_gcp_public_datasets,
    }

    # Iterate over all results
    for response_item in client.search_catalog(scope, query):
        print(
            u"Result type: {}".format(
                enums.SearchResultType(response_item.search_result_type).name
            )
        )
        print(u"Result subtype: {}".format(response_item.search_result_subtype))
        print(
            u"Relative resource name: {}".format(response_item.relative_resource_name)
        )
        print(u"Linked resource: {}\n".format(response_item.linked_resource))


# [END datacatalog_search]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--include_project_id", type=str, default="[Google Cloud Project ID]"
    )
    parser.add_argument("--include_gcp_public_datasets", type=bool, default=False)
    parser.add_argument("--query", type=str, default="[String in search query syntax]")
    args = parser.parse_args()

    sample_search_catalog(
        args.include_project_id, args.include_gcp_public_datasets, args.query
    )


if __name__ == "__main__":
    main()
