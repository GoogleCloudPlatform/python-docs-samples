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


def create_interaction() -> str:
    # [START googlegenaisdk_interactions_textgen_with_mute_video]
    from google import genai
    from google.genai.interactions import TextContent, VideoContent

    client = genai.Client()
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=[
            VideoContent(
                uri="gs://cloud-samples-data/generative-ai/video/ad_copy_from_video.mp4",
                mime_type="video/mp4",
            ),
            TextContent(text="What is in the video?"),
        ],
    )
    print(interaction.output_text)
    # Example response:
    # The video shows several people surfing in an ocean with a coastline in the background. The camera ...
    # [END googlegenaisdk_interactions_textgen_with_mute_video]
    return interaction.output_text


if __name__ == "__main__":
    create_interaction()
