# # Copyright 2024 Google LLC
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #     http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.
# #
#
#
# def create_target_site(
#     project_id: str,
#     location: str,
#     data_store_id: str,
#     uri_pattern: str,
# ):
#     # [START genappbuilder_create_target_site]
#     from google.api_core.client_options import ClientOptions
#
#     from google.cloud import discoveryengine_v1 as discoveryengine
#
#     # TODO(developer): Uncomment these variables before running the sample.
#     # project_id = "YOUR_PROJECT_ID"
#     # location = "YOUR_LOCATION" # Values: "global"
#     # data_store_id = "YOUR_DATA_STORE_ID"
#     # NOTE: Do not include http or https protocol in the URI pattern
#     # uri_pattern = "cloud.google.com/generative-ai-app-builder/docs/*"
#
#     #  For more information, refer to:
#     # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
#     client_options = (
#         ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
#         if location != "global"
#         else None
#     )
#
#     # Create a client
#     client = discoveryengine.SiteSearchEngineServiceClient(
#         client_options=client_options
#     )
#
#     # The full resource name of the data store
#     # e.g. projects/{project}/locations/{location}/dataStores/{data_store_id}
#     site_search_engine = client.site_search_engine_path(
#         project=project_id, location=location, data_store=data_store_id
#     )
#
#     # Target Site to index
#     target_site = discoveryengine.TargetSite(
#         provided_uri_pattern=uri_pattern,
#         # Options: INCLUDE, EXCLUDE
#         type_=discoveryengine.TargetSite.Type.INCLUDE,
#         exact_match=False,
#     )
#
#     # Make the request
#     operation = client.create_target_site(
#         parent=site_search_engine,
#         target_site=target_site,
#     )
#
#     print(f"Waiting for operation to complete: {operation.operation.name}")
#     response = operation.result()
#
#     # After the operation is complete,
#     # get information from operation metadata
#     metadata = discoveryengine.CreateTargetSiteMetadata(operation.metadata)
#
#     # Handle the response
#     print(response)
#     print(metadata)
#     # [END genappbuilder_create_target_site]
#
#     return response
#
#
# def delete_target_site(
#     project_id: str,
#     location: str,
#     data_store_id: str,
#     target_site_id: str,
# ):
#     # [START genappbuilder_delete_target_site]
#     from google.api_core.client_options import ClientOptions
#
#     from google.cloud import discoveryengine_v1 as discoveryengine
#
#     # TODO(developer): Uncomment these variables before running the sample.
#     # project_id = "YOUR_PROJECT_ID"
#     # location = "YOUR_LOCATION" # Values: "global"
#     # data_store_id = "YOUR_DATA_STORE_ID"
#     # target_site_id = "YOUR_TARGET_SITE_ID"
#
#     #  For more information, refer to:
#     # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
#     client_options = (
#         ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
#         if location != "global"
#         else None
#     )
#
#     # Create a client
#     client = discoveryengine.SiteSearchEngineServiceClient(
#         client_options=client_options
#     )
#
#     # The full resource name of the data store
#     # e.g. projects/{project}/locations/{location}/collections/{collection}/dataStores/{data_store_id}/siteSearchEngine/targetSites/{target_site}
#     name = client.target_site_path(
#         project=project_id,
#         location=location,
#         data_store=data_store_id,
#         target_site=target_site_id,
#     )
#
#     # Make the request
#     operation = client.delete_target_site(name=name)
#
#     print(f"Operation: {operation.operation.name}")
#     # [END genappbuilder_delete_target_site]
#
#     return operation.operation.name
