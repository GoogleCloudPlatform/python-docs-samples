# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def transcript_audio() -> str:
    """Transcribes the content of an audio file using a pre-trained generative model."""
    # [START generativeaionvertexai_gemini_audio_transcription]

    import vertexai
    from vertexai.generative_models import GenerativeModel, GenerationConfig, Part

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"

    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-002")

    prompt = """
    Can you transcribe this interview, in the format of timecode, speaker, caption.
    Use speaker A, speaker B, etc. to identify speakers.
    """

    audio_file_uri = "gs://cloud-samples-data/generative-ai/audio/pixel.mp3"
    audio_file = Part.from_uri(audio_file_uri, mime_type="audio/mpeg")

    contents = [audio_file, prompt]

    response = model.generate_content(contents, generation_config=GenerationConfig(audio_timestamp=True))

    print(response.text)
    # Example response:
    # [00:00:00] Speaker A: Your devices are getting better over time...
    # [00:00:16] Speaker B: Welcome to the Made by Google podcast, ...
    # [00:01:00] Speaker A: So many features. I am a singer. ...
    # [00:01:33] Speaker B: Amazing. DeCarlos, same question to you, ...

    # [END generativeaionvertexai_gemini_audio_transcription]
    return response.text


if __name__ == "__main__":
    transcript_audio()
