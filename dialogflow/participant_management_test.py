# Copyright 2021 Google LLC
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

import os

import conversation_management
import conversation_profile_management
import document_management
import knowledge_base_management
import participant_management

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
KNOWLEDGE_BASE_DISPLAY_NAME = "fake_KNOWLEDGE_BASE_DISPLAY_NAME"
DOCUMENT_DISPLAY_NAME = "Cancel an order"
CONVERSATION_PROFILE_DISPLAY_NAME = "fake_conversation_profile"


def test_analyze_content_text(capsys):
    """Test analyze content api with text only messages."""
    # Create knowledge base.
    knowledge_base_management.create_knowledge_base(
        PROJECT_ID, KNOWLEDGE_BASE_DISPLAY_NAME
    )
    out, _ = capsys.readouterr()
    knowledge_base_id = out.split("knowledgeBases/")[1].rstrip()
    # Get the knowledge base
    knowledge_base_management.get_knowledge_base(PROJECT_ID, knowledge_base_id)

    out, _ = capsys.readouterr()
    assert "Display Name: {}".format(KNOWLEDGE_BASE_DISPLAY_NAME) in out

    # Create documents. Note that you should get read permission of bucket gs://cloud-samples-data/dialogflow/participant_test.html
    # via Pantheon for service account (google application credential account) from here:
    # https://support.google.com/googleshopping/answer/9116497
    document_management.create_document(
        PROJECT_ID,
        knowledge_base_id,
        DOCUMENT_DISPLAY_NAME,
        "text/html",
        "ARTICLE_SUGGESTION",
        "gs://cloud-samples-data/dialogflow/participant_test.html",
    )
    out, _ = capsys.readouterr()
    document_id = out.split("documents/")[1].split(" - MIME Type:")[0].rstrip()

    # Get the Document
    document_management.get_document(PROJECT_ID, knowledge_base_id, document_id)

    out, _ = capsys.readouterr()
    assert "Display Name: {}".format(DOCUMENT_DISPLAY_NAME) in out

    # Create conversation profile.
    conversation_profile_management.create_conversation_profile_article_faq(
        project_id=PROJECT_ID,
        display_name=CONVERSATION_PROFILE_DISPLAY_NAME,
        article_suggestion_knowledge_base_id=knowledge_base_id,
    )

    out, _ = capsys.readouterr()
    assert "Display Name: {}".format(CONVERSATION_PROFILE_DISPLAY_NAME) in out
    conversation_profile_id = out.split("conversationProfiles/")[1].rstrip()

    # Create conversation.
    conversation_management.create_conversation(
        project_id=PROJECT_ID, conversation_profile_id=conversation_profile_id
    )

    out, _ = capsys.readouterr()
    conversation_id = out.split("conversations/")[1].rstrip()

    # Create end user participant.
    participant_management.create_participant(
        project_id=PROJECT_ID, conversation_id=conversation_id, role="END_USER"
    )
    out, _ = capsys.readouterr()
    end_user_id = out.split("participants/")[1].rstrip()

    # Create human agent participant.
    participant_management.create_participant(
        project_id=PROJECT_ID, conversation_id=conversation_id, role="HUMAN_AGENT"
    )
    out, _ = capsys.readouterr()
    human_agent_id = out.split("participants/")[1].rstrip()

    # AnalyzeContent
    participant_management.analyze_content_text(
        project_id=PROJECT_ID,
        conversation_id=conversation_id,
        participant_id=human_agent_id,
        text="Hi, how are you?",
    )
    out, _ = capsys.readouterr()

    participant_management.analyze_content_text(
        project_id=PROJECT_ID,
        conversation_id=conversation_id,
        participant_id=end_user_id,
        text="Hi, I am doing well, how about you?",
    )
    out, _ = capsys.readouterr()

    participant_management.analyze_content_text(
        project_id=PROJECT_ID,
        conversation_id=conversation_id,
        participant_id=human_agent_id,
        text="Great. How can I help you?",
    )
    out, _ = capsys.readouterr()

    participant_management.analyze_content_text(
        project_id=PROJECT_ID,
        conversation_id=conversation_id,
        participant_id=end_user_id,
        text="So I ordered something, but I do not like it.",
    )
    out, _ = capsys.readouterr()

    participant_management.analyze_content_text(
        project_id=PROJECT_ID,
        conversation_id=conversation_id,
        participant_id=end_user_id,
        text="Thinking if I can cancel that order",
    )
    suggestion_out, _ = capsys.readouterr()
    # Currently suggestion_out won't contain the suggestion we want since it
    # takes time for document to be ready to serve.
    # assert 'Cancel an order' in suggestion_out

    # Complete conversation.
    conversation_management.complete_conversation(
        project_id=PROJECT_ID, conversation_id=conversation_id
    )

    # Delete conversation profile.
    conversation_profile_management.delete_conversation_profile(
        project_id=PROJECT_ID, conversation_profile_id=conversation_profile_id
    )

    # Delete document.
    document_management.delete_document(PROJECT_ID, knowledge_base_id, document_id)

    # Delete the Knowledge Base.
    knowledge_base_management.delete_knowledge_base(PROJECT_ID, knowledge_base_id)
