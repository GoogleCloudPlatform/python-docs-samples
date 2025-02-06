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

# !This sample works with Google Cloud Vertex AI API only.


def generate_content() -> str:
    # [START googlegenaisdk_textgen_with_youtube_video]
    from google import genai
    from google.genai import types

    client = genai.Client()
    model_id = "gemini-2.0-flash-exp"

    # You can include text, PDF documents, images, audio and video in your prompt requests and get text or code responses.
    video = types.Part.from_uri(
        file_uri="https://www.youtube.com/watch?v=3KtWfp0UopM",
        mime_type="video/mp4",
    )

    response = client.models.generate_content(
        model=model_id,
        contents=[
            video,
            "Write a short and engaging blog post based on this video.",
        ],
    )

    print(response.text)
    # Example response:
    # Lunchtime Level Up: Easy & Delicious Meal Prep
    # We all know the struggle:  you're rushing in the morning, and lunch is the
    # last thing on your mind...

    # [END googlegenaisdk_textgen_with_youtube_video]
    return response.text


if __name__ == "__main__":
    generate_content()
