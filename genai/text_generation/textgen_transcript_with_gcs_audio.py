# Copyright 2025 Google LLC
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


def generate_content() -> str:
    # [START googlegenaisdk_textgen_transcript_with_gcs_audio]
    from google import genai
    from google.genai.types import GenerateContentConfig, HttpOptions, Part

    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    prompt = """
    Transcribe the interview, in the format of timecode, speaker, caption.
    Use speaker A, speaker B, etc. to identify speakers.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        contents=[
            prompt,
            Part.from_uri(
                file_uri="gs://cloud-samples-data/generative-ai/audio/pixel.mp3",
                mime_type="audio/mpeg",
            ),
        ],
        # Required to enable timestamp understanding for audio-only files
        config=GenerateContentConfig(audio_timestamp=True),
    )
    print(response.text)
    # Example response:
    # [00:00:00] **Speaker A:** your devices are getting better over time. And so ...
    # [00:00:14] **Speaker B:** Welcome to the Made by Google podcast where we meet ...
    # [00:00:20] **Speaker B:** Here's your host, Rasheed Finch.
    # [00:00:23] **Speaker C:** Today we're talking to Aisha Sharif and DeCarlos Love. ...
    # ...
    # [END googlegenaisdk_textgen_transcript_with_gcs_audio]
    return response.text


if __name__ == "__main__":
    generate_content()
