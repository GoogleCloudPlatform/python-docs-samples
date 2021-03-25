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

import answer_record_management
import conversation_management
import conversation_profile_management
import participant_management

PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
SMART_REPLY_MODEL = os.getenv('SMART_REPLY_MODEL')
SMART_REPLY_ALLOWLIST = os.getenv('SMART_REPLY_ALLOWLIST')
CONVERSATION_PROFILE_DISPLAY_NAME = 'sample code profile for smart reply'


def test_smart_reply(capsys):
    """Test smart reply feature.
    """

    # Create conversation profile.
    conversation_profile_management.create_conversation_profile_smart_reply(
        project_id=PROJECT_ID,
        display_name=CONVERSATION_PROFILE_DISPLAY_NAME,
        smart_reply_allowlist_name=SMART_REPLY_ALLOWLIST,
        smart_reply_model_name=SMART_REPLY_MODEL)

    out, _ = capsys.readouterr()
    assert 'Display Name: {}'.format(CONVERSATION_PROFILE_DISPLAY_NAME) in out
    conversation_profile_id = out.split('conversationProfiles/')[1].rstrip()

    # Create conversation.
    conversation_management.create_conversation(
        project_id=PROJECT_ID, conversation_profile_id=conversation_profile_id)

    out, _ = capsys.readouterr()
    conversation_id = out.split('conversations/')[1].rstrip()

    # Create end user participant.
    participant_management.create_participant(project_id=PROJECT_ID,
                                              conversation_id=conversation_id,
                                              role='END_USER')
    out, _ = capsys.readouterr()
    end_user_id = out.split('participants/')[1].rstrip()

    # Create human agent participant.
    participant_management.create_participant(project_id=PROJECT_ID,
                                              conversation_id=conversation_id,
                                              role='HUMAN_AGENT')
    out, _ = capsys.readouterr()
    human_agent_id = out.split('participants/')[1].rstrip()

    # AnalyzeContent
    participant_management.analyze_content_text(
        project_id=PROJECT_ID,
        conversation_id=conversation_id,
        participant_id=human_agent_id,
        text='Hi, how are you?')
    out, _ = capsys.readouterr()
    assert 'What would you like to know?' in out

    response = participant_management.analyze_content_text(
        project_id=PROJECT_ID,
        conversation_id=conversation_id,
        participant_id=end_user_id,
        text='I am doing well, just want to check')
    out, _ = capsys.readouterr()
    assert 'Sounds good.' in out
    # Update AnswerRecord.
    answer_record_id = response.human_agent_suggestion_results[
        0].suggest_smart_replies_response.smart_reply_answers[
            0].answer_record.split('answerRecords/')[1].rstrip()
    answer_record_management.update_answer_record(
        project_id=PROJECT_ID,
        answer_record_id=answer_record_id,
        is_clicked=True)
    out, _ = capsys.readouterr()
    assert 'Clicked: True' in out

    # Complete conversation.
    conversation_management.complete_conversation(
        project_id=PROJECT_ID, conversation_id=conversation_id)

    # Delete conversation profile.
    conversation_profile_management.delete_conversation_profile(
        project_id=PROJECT_ID, conversation_profile_id=conversation_profile_id)
