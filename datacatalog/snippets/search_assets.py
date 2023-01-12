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


def search_assets(override_values):
    """Searches Data Catalog entries for a given project."""
    # [START data_catalog_search_assets]
    from google.cloud import datacatalog_v1

    datacatalog = datacatalog_v1.DataCatalogClient()

    # TODO: Set these values before running the sample.
    project_id = "project_id"

    # Set custom query.
    search_string = "type=dataset"
    # [END data_catalog_search_assets]

    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    project_id = override_values.get("project_id", project_id)
    tag_template_id = override_values.get("tag_template_id", search_string)
    search_string = f"name:{tag_template_id}"

    # [START data_catalog_search_assets]
    scope = datacatalog_v1.types.SearchCatalogRequest.Scope()
    scope.include_project_ids.append(project_id)

    # Alternatively, search using organization scopes.
    # scope.include_org_ids.append("my_organization_id")

    search_results = datacatalog.search_catalog(scope=scope, query=search_string)

    print("Results in project:")
    for result in search_results:
        print(result)
    # [END data_catalog_search_assets]
