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
#   description: Search Catalog
#   usage: python3 samples/v1beta1/datacatalog_search.py [--include_project_id "[Google Cloud Project ID]"] [--include_gcp_public_datasets false] [--query "[String in search query syntax]"]


def sample_search_catalog(
    include_project_id: str, include_gcp_public_datasets: bool, query: str
):
    # [START data_catalog_search_v1beta1]
    from google.cloud import datacatalog_v1beta1

    """
    Search Catalog

    Args:
      include_project_id (str): Your Google Cloud project ID.
      include_gcp_public_datasets (bool): If true, include Google Cloud Platform (GCP) public
      datasets in the search results.
      query (str): Your query string.
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
    results = client.search_catalog(request={"scope": scope, "query": query})
    for response_item in results:
        print(
            f"Result type: {datacatalog_v1beta1.SearchResultType(response_item.search_result_type).name}"
        )
        print(f"Result subtype: {response_item.search_result_subtype}")
        print(f"Relative resource name: {response_item.relative_resource_name}")
        print(f"Linked resource: {response_item.linked_resource}\n")
    # [END data_catalog_search_v1beta1]
    return results


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
