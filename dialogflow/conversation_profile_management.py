#!/usr/bin/env python

# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""Dialogflow API Python sample showing how to manage Conversation Profiles.
"""

from google.cloud import dialogflow_v2beta1 as dialogflow


# [START dialogflow_list_conversation_profiles]
def list_conversation_profiles(project_id):
    """Lists the conversation profiles belonging to a project.

    Args: project_id: The GCP project linked with the conversation profile."""

    client = dialogflow.ConversationProfilesClient()
    project_path = client.common_project_path(project_id)
    response = client.list_conversation_profiles(parent=project_path)
    for conversation_profile in response:
        print("Display Name: {}".format(conversation_profile.display_name))
        print("Name: {}".format(conversation_profile.name))
    return response


# [END dialogflow_list_conversation_profiles]


# [START dialogflow_create_conversation_profile_article_faq]
def create_conversation_profile_article_faq(
    project_id,
    display_name,
    article_suggestion_knowledge_base_id=None,
    faq_knowledge_base_id=None,
):
    """Creates a conversation profile with given values

    Args: project_id:  The GCP project linked with the conversation profile.
        display_name: The display name for the conversation profile to be
        created.
        article_suggestion_knowledge_base_id: knowledge base id for article
        suggestion.
        faq_knowledge_base_id: knowledge base id for faq."""

    client = dialogflow.ConversationProfilesClient()
    project_path = client.common_project_path(project_id)

    conversation_profile = {
        "display_name": display_name,
        "human_agent_assistant_config": {
            "human_agent_suggestion_config": {"feature_configs": []}
        },
        "language_code": "en-US",
    }

    if article_suggestion_knowledge_base_id is not None:
        as_kb_path = dialogflow.KnowledgeBasesClient.knowledge_base_path(
            project_id, article_suggestion_knowledge_base_id
        )
        feature_config = {
            "suggestion_feature": {"type_": "ARTICLE_SUGGESTION"},
            "suggestion_trigger_settings": {
                "no_small_talk": True,
                "only_end_user": True,
            },
            "query_config": {
                "knowledge_base_query_source": {"knowledge_bases": [as_kb_path]},
                "max_results": 3,
            },
        }
        conversation_profile["human_agent_assistant_config"][
            "human_agent_suggestion_config"
        ]["feature_configs"].append(feature_config)
    if faq_knowledge_base_id is not None:
        faq_kb_path = dialogflow.KnowledgeBasesClient.knowledge_base_path(
            project_id, faq_knowledge_base_id
        )
        feature_config = {
            "suggestion_feature": {"type_": "FAQ"},
            "suggestion_trigger_settings": {
                "no_small_talk": True,
                "only_end_user": True,
            },
            "query_config": {
                "knowledge_base_query_source": {"knowledge_bases": [faq_kb_path]},
                "max_results": 3,
            },
        }
        conversation_profile["human_agent_assistant_config"][
            "human_agent_suggestion_config"
        ]["feature_configs"].append(feature_config)

    response = client.create_conversation_profile(
        parent=project_path, conversation_profile=conversation_profile
    )

    print("Conversation Profile created:")
    print("Display Name: {}".format(response.display_name))
    # Put Name is the last to make it easier to retrieve.
    print("Name: {}".format(response.name))
    return response


# [END dialogflow_create_conversation_profile_article_faq]


# [START dialogflow_create_conversation_profile_smart_reply]
def create_conversation_profile_smart_reply(
    project_id, display_name, smart_reply_allowlist_name, smart_reply_model_name
):
    """Creates a conversation profile with given values for smart reply

    Args: project_id:  The GCP project linked with the conversation profile.
        display_name: The display name for the conversation profile to be
        created.
        smart_reply_allowlist_name: document name for smart reply allowlist.
        smart_reply_model_name: conversation model name for smart reply."""

    client = dialogflow.ConversationProfilesClient()
    project_path = client.common_project_path(project_id)

    conversation_profile = {
        "display_name": display_name,
        "human_agent_assistant_config": {
            "human_agent_suggestion_config": {"feature_configs": []}
        },
        "language_code": "en-US",
    }
    feature_config = {
        "suggestion_feature": {"type_": "SMART_REPLY"},
        "suggestion_trigger_settings": {
            "no_small_talk": True,
            "only_end_user": True,
        },
        "query_config": {
            "document_query_source": {"documents": [smart_reply_allowlist_name]},
            "max_results": 3,
        },
        "conversation_model_config": {"model": smart_reply_model_name},
    }
    conversation_profile["human_agent_assistant_config"][
        "human_agent_suggestion_config"
    ]["feature_configs"].append(feature_config)

    response = client.create_conversation_profile(
        parent=project_path, conversation_profile=conversation_profile
    )

    print("Conversation Profile created:")
    print("Display Name: {}".format(response.display_name))
    # Put Name is the last to make it easier to retrieve.
    print("Name: {}".format(response.name))
    return response


# [END dialogflow_create_conversation_profile_smart_reply]


# [START dialogflow_get_conversation_profile]
def get_conversation_profile(project_id, conversation_profile_id):
    """Gets a specific conversation profile.

    Args: project_id: The GCP project linked with the conversation profile.
        conversation_profile_id: Id of the conversation profile."""

    client = dialogflow.ConversationProfilesClient()
    conversation_profile_path = client.conversation_profile_path(
        project_id, conversation_profile_id
    )

    response = client.get_conversation_profile(name=conversation_profile_path)

    print("Got conversation profile:")
    print("Display Name: {}".format(response.display_name))
    print("Name: {}".format(response.name))
    return response


# [END dialogflow_get_conversation_profile]


# [START dialogflow_delete_conversation_profile]
def delete_conversation_profile(project_id, conversation_profile_id):
    """Deletes a specific conversation profile.

    Args: project_id: The GCP project linked with the conversation profile.
        conversation_profile_id: Id of the conversation profile."""

    client = dialogflow.ConversationProfilesClient()
    conversation_profile_path = client.conversation_profile_path(
        project_id, conversation_profile_id
    )

    client.delete_conversation_profile(name=conversation_profile_path)

    print("Conversation Profile deleted.")


# [END dialogflow_delete_conversation_profile]
