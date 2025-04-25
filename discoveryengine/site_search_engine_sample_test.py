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
# import os
# import re
#
# from discoveryengine import site_search_engine_sample
#
# project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
# location = "global"
# data_store_id = "site-search-data-store"
#
#
# def test_create_target_site():
#     response = site_search_engine_sample.create_target_site(
#         project_id,
#         location,
#         data_store_id,
#         uri_pattern="cloud.google.com/generative-ai-app-builder/docs/*",
#     )
#     assert response, response
#     match = re.search(r"\/targetSites\/([^\/]+)", response.name)
#
#     if match:
#         target_site = match.group(1)
#         site_search_engine_sample.delete_target_site(
#             project_id=project_id,
#             location=location,
#             data_store_id=data_store_id,
#             target_site_id=target_site,
#         )
