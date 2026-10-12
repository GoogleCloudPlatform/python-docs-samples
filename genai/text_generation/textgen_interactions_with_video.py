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
    # [START googlegenaisdk_interactions_textgen_with_video]
    from google import genai

    client = genai.Client()
    prompt = """
    Analyze the provided video file, including its audio.
    Summarize the main points of the video concisely.
    Create a chapter breakdown with timestamps for key sections or topics discussed.
    """
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=[
            {
                "type": "video",
                "uri": "gs://cloud-samples-data/generative-ai/video/pixel8.mp4",
                "mime_type": "video/mp4",
            },
            {"text": prompt},
        ],
    )

    print(interaction.output_text)
    # Example response:
    # Here's a breakdown of the video:
    #
    # **Summary:**
    #
    # Saeka Shimada, a photographer in Tokyo, uses the Google Pixel 8 Pro's "Video Boost" feature to ...
    #
    # **Chapter Breakdown with Timestamps:**
    #
    # * **[00:00-00:12] Introduction & Tokyo at Night:** Saeka Shimada introduces herself ...
    # ...
    # [END googlegenaisdk_interactions_textgen_with_video]
    return interaction.output_text


if __name__ == "__main__":
    generate_content()
