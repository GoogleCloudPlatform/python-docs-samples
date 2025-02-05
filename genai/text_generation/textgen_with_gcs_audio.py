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
    # [START googlegenaisdk_textgen_with_gcs_audio]
    from google import genai
    from google.genai.types import Part

    client = genai.Client()

    prompt = """
    Provide the summary of the audio file.
    Summarize the main points of the audio concisely.
    Create a chapter breakdown with timestamps for key sections or topics discussed.
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=[
            prompt,
            Part.from_uri(
                file_uri="gs://cloud-samples-data/generative-ai/audio/pixel.mp3",
                mime_type="audio/mpeg",
            ),
        ],
    )
    print(response.text)
    # Example response:
    # This episode of the Made by Google podcast features product managers ...
    #
    # **Chapter Breakdown:**
    #
    # * **[0:00-1:14] Introduction:** Host Rasheed Finch introduces Aisha and DeCarlos and ...
    # * **[1:15-2:44] Transformative Features:** Aisha and DeCarlos discuss their ...
    # ...
    # [END googlegenaisdk_textgen_with_gcs_audio]
    return response.text


if __name__ == "__main__":
    generate_content()
