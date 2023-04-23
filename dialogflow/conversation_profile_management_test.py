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

import conversation_profile_management

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

CONVERSATION_PROFILE_DISPLAY_NAME = "fake_conversation_profile_name"


def test_create_conversation_profile(capsys):
    # Check the conversation profile does not yet exists.
    conversation_profile_management.list_conversation_profiles(PROJECT_ID)

    out, _ = capsys.readouterr()
    assert f"Display Name: {CONVERSATION_PROFILE_DISPLAY_NAME}" not in out

    # Create a conversation profile.
    conversation_profile_management.create_conversation_profile_article_faq(
        project_id=PROJECT_ID,
        display_name=CONVERSATION_PROFILE_DISPLAY_NAME,
        article_suggestion_knowledge_base_id="abc",
    )
    out, _ = capsys.readouterr()
    assert f"Display Name: {CONVERSATION_PROFILE_DISPLAY_NAME}" in out

    conversation_profile_id = out.split("conversationProfiles/")[1].rstrip()

    # List conversation profiles.
    conversation_profile_management.list_conversation_profiles(PROJECT_ID)

    out, _ = capsys.readouterr()
    assert f"Display Name: {CONVERSATION_PROFILE_DISPLAY_NAME}" in out

    # Get the conversation profile.
    conversation_profile_management.get_conversation_profile(
        PROJECT_ID, conversation_profile_id
    )

    out, _ = capsys.readouterr()
    assert f"Display Name: {CONVERSATION_PROFILE_DISPLAY_NAME}" in out

    # Delete the conversation profile.
    conversation_profile_management.delete_conversation_profile(
        PROJECT_ID, conversation_profile_id
    )

    # Verify the conversation profile is deleted.
    conversation_profile_management.list_conversation_profiles(PROJECT_ID)

    out, _ = capsys.readouterr()
    assert f"Display Name: {CONVERSATION_PROFILE_DISPLAY_NAME}" not in out
