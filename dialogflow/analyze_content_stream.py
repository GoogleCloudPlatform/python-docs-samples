# Copyright 2025 Google LLC
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

"""Google Cloud Dialogflow API sample code using the StreamingAnalyzeContent
API.

Also please contact Google to get credentials of this project and set up the
credential file json locations by running:
export GOOGLE_APPLICATION_CREDENTIALS=<cred_json_file_location>

Example usage:
    export GOOGLE_CLOUD_PROJECT='cloud-contact-center-ext-demo'
    export CONVERSATION_PROFILE='FnuBYO8eTBWM8ep1i-eOng'
    export GOOGLE_APPLICATION_CREDENTIALS='/Users/ruogu/Desktop/keys/cloud-contact-center-ext-demo-78798f9f9254.json'
    export AUDIO_FILE_PATH='/Users/ruogu/Desktop/book_a_room.wav'

    python analyze_content_stream.py

"""

import os
import conversation_management
import participant_management
from pydub import AudioSegment
import math

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
AUDIO_FILE_PATH = os.getenv("AUDIO_FILE_PATH")
CONVERSATION_PROFILE_ID = os.getenv("CONVERSATION_PROFILE")


def split_audio(audio_file_path, max_length_ms=5_000):
    """Splits audio into chunks under max_length_ms."""
    audio = AudioSegment.from_file(audio_file_path)
    chunks = []
    num_chunks = math.ceil(len(audio) / max_length_ms)
    base_filename = os.path.splitext(audio_file_path)[0]

    for i in range(num_chunks):
        start = i * max_length_ms
        end = min((i + 1) * max_length_ms, len(audio))
        chunk = audio[start:end]
        chunk_path = f"{base_filename}_part{i}.wav"
        chunk.export(chunk_path, format="wav", parameters=["-ac", "1"])
        chunks.append(chunk_path)

    return chunks

def run_analyze_content_streaming(conversation_profile_id, audio_file_path, project_id):
    # Create conversation
    conversation = conversation_management.create_conversation(
        project_id=project_id,
        conversation_profile_id=conversation_profile_id
    )
    conversation_id = conversation.name.split("conversations/")[1]

    # Create participant
    participant = participant_management.create_participant(
        project_id=project_id,
        conversation_id=conversation_id,
        role="END_USER"
    )
    participant_id = participant.name.split("participants/")[1]

    class stream_generator:
        def __init__(self, audio_file_path):
            self.audio_file_path = audio_file_path

        def generator(self):
            with open(self.audio_file_path, "rb") as audio_file:
                while True:
                    chunk = audio_file.read(10000)
                    if not chunk:
                        break
                    # The later requests contains audio data.
                    yield chunk

    results = participant_management.analyze_content_audio_stream(
        conversation_id=conversation_id,
        participant_id=participant_id,
        sample_rate_herz=48000,
        stream=stream_generator(audio_file_path),
        language_code="en-US",
        timeout=300,
    )

    out = " ".join([result.message.content for result in results])    
    
    print(f"🔊 Transcription: {out}")

    # Complete conversation
    conversation_management.complete_conversation(project_id, conversation_id)
    return out

if __name__ == "__main__":
    audio_chunks = split_audio(AUDIO_FILE_PATH)
    results = []
    for chunk_path in audio_chunks:
        print(f"Processing {chunk_path}...")
        partial_result = run_analyze_content_streaming(CONVERSATION_PROFILE_ID, chunk_path, PROJECT_ID)
        results.extend(partial_result)
    
    print("Final Transcript: {}".format(''.join(results).strip()))