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
    # [START googlegenaisdk_interactions_textgen_with_youtube_video]
    from google import genai

    client = genai.Client()
    model_id = "gemini-3.8-flash"

    interaction = client.interactions.create(
        model=model_id,
        input=[
            {
                "type": "video",
                "uri": "https://www.youtube.com/watch?v=3KtWfp0UopM",
                "mime_type": "video/mp4",
            },
            {"text": "Write a short and engaging blog post based on this video."},
        ],
    )

    print(interaction.output_text)
    # Example response:
    # Here's a short blog post based on the video provided:
    #
    # **Google Turns 25: A Quarter Century of Search!**
    # ...

    # [END googlegenaisdk_interactions_textgen_with_youtube_video]
    return interaction.output_text


if __name__ == "__main__":
    generate_content()
