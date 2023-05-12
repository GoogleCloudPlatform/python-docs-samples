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

import os
import uuid

import pytest

import conversation_management
import conversation_profile_management
import participant_management

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
AUDIO_FILE_PATH = "{0}/resources/book_a_room.wav".format(
    os.path.realpath(os.path.dirname(__file__)),
)


@pytest.fixture
def conversation_profile_display_name():
    return f"sample_conversation_profile_{uuid.uuid4()}"


@pytest.fixture
def conversation_profile_id(conversation_profile_display_name):
    # Create conversation profile.
    response = conversation_profile_management.create_conversation_profile_article_faq(
        project_id=PROJECT_ID, display_name=conversation_profile_display_name
    )
    conversation_profile_id = response.name.split("conversationProfiles/")[1].rstrip()

    yield conversation_profile_id

    # Delete the conversation profile.
    conversation_profile_management.delete_conversation_profile(
        PROJECT_ID, conversation_profile_id
    )


@pytest.fixture
def conversation_id(conversation_profile_id):
    # Create conversation.
    response = conversation_management.create_conversation(
        project_id=PROJECT_ID, conversation_profile_id=conversation_profile_id
    )
    conversation_id = response.name.split("conversations/")[1].rstrip()

    yield conversation_id

    # Complete the conversation.
    conversation_management.complete_conversation(
        project_id=PROJECT_ID, conversation_id=conversation_id
    )


@pytest.fixture
def participant_id(conversation_id):
    response = participant_management.create_participant(
        project_id=PROJECT_ID, conversation_id=conversation_id, role="END_USER"
    )
    participant_id = response.name.split("participants/")[1].rstrip()
    yield participant_id


# Test live transcription of an audio file with streaming_analyze_content.
def test_analyze_content_audio(capsys, conversation_id, participant_id):
    # Call StreamingAnalyzeContent to transcribe the audio.
    participant_management.analyze_content_audio(
        conversation_id=conversation_id,
        participant_id=participant_id,
        audio_file_path=AUDIO_FILE_PATH,
    )
    out, _ = capsys.readouterr()
    assert "book a room" in out.lower()


# Test live transcription of an audio stream with streaming_analyze_content.
def test_analyze_content_audio_stream(capsys, conversation_id, participant_id):
    class stream_generator():
        def __init__(self, audio_file_path):
            self.audio_file_path = audio_file_path

        def generator(self):
            with open(self.audio_file_path, "rb") as audio_file:
                while True:
                    chunk = audio_file.read(4096)
                    if not chunk:
                        break
                    # The later requests contains audio data.
                    yield chunk
    # Call StreamingAnalyzeContent to transcribe the audio.
    responses = participant_management.analyze_content_audio_stream(
        conversation_id=conversation_id,
        participant_id=participant_id,
        sample_rate_herz=16000,
        stream=stream_generator(AUDIO_FILE_PATH),
        language_code="en-US",
        timeout=300
    )
    for response in responses:
        print(response)
    out, _ = capsys.readouterr()
    assert "book a room" in out.lower()
