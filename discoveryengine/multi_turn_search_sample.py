# Copyright 2023 Google LLC
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

# [START genappbuilder_multi_turn_search]
from typing import List

from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine

# TODO(developer): Uncomment these variables before running the sample.
# project_id = "YOUR_PROJECT_ID"
# location = "YOUR_LOCATION"                    # Values: "global", "us", "eu"
# data_store_id = "YOUR_DATA_STORE_ID"
# search_queries = ["YOUR_FIRST_SEARCH_QUERY", "YOUR_SECOND_SEARCH_QUERY"]


def multi_turn_search_sample(
    project_id: str,
    location: str,
    data_store_id: str,
    search_queries: List[str],
) -> List[discoveryengine.ConverseConversationResponse]:
    #  For more information, refer to:
    # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    # Create a client
    client = discoveryengine.ConversationalSearchServiceClient(
        client_options=client_options
    )

    # Initialize Multi-Turn Session
    conversation = client.create_conversation(
        # The full resource name of the data store
        # e.g. projects/{project_id}/locations/{location}/dataStores/{data_store_id}
        parent=client.data_store_path(
            project=project_id, location=location, data_store=data_store_id
        ),
        conversation=discoveryengine.Conversation(),
    )

    # [END genappbuilder_multi_turn_search]
    # For testing only
    responses: List[discoveryengine.ConverseConversationResponse] = []
    # [START genappbuilder_multi_turn_search]

    for search_query in search_queries:
        # Add new message to session
        request = discoveryengine.ConverseConversationRequest(
            name=conversation.name,
            query=discoveryengine.TextInput(input=search_query),
            serving_config=client.serving_config_path(
                project=project_id,
                location=location,
                data_store=data_store_id,
                serving_config="default_config",
            ),
            # Options for the returned summary
            summary_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec(
                # Number of results to include in summary
                summary_result_count=3,
                include_citations=True,
            ),
        )
        response = client.converse_conversation(request)

        print(f"Reply: {response.reply.summary.summary_text}\n")

        for i, result in enumerate(response.search_results, 1):
            result_data = result.document.derived_struct_data
            print(f"[{i}]")
            print(f"Link: {result_data['link']}")
            print(f"First Snippet: {result_data['snippets'][0]['snippet']}")
            print(
                "First Extractive Answer: \n"
                f"\tPage: {result_data['extractive_answers'][0]['pageNumber']}\n"
                f"\tContent: {result_data['extractive_answers'][0]['content']}\n\n"
            )
        print("\n\n")

        # [END genappbuilder_multi_turn_search]
        responses.append(response)

    return responses
