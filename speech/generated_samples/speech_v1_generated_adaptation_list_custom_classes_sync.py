# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Generated code. DO NOT EDIT!
#
# Snippet for ListCustomClasses
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-speech


# [START speech_v1_generated_Adaptation_ListCustomClasses_sync]
from google.cloud import speech_v1


def sample_list_custom_classes():
    # Create a client
    client = speech_v1.AdaptationClient()

    # Initialize request argument(s)
    request = speech_v1.ListCustomClassesRequest(
        parent="parent_value",
    )

    # Make the request
    page_result = client.list_custom_classes(request=request)

    # Handle the response
    for response in page_result:
        print(response)

# [END speech_v1_generated_Adaptation_ListCustomClasses_sync]
