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

# !This sample works with Google Cloud Vertex AI API only.


def generate_content() -> str:
    # [START googlegenaisdk_textgen_with_youtube_video]
    from google import genai
    from google.genai.types import HttpOptions, Part

    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    model_id = "gemini-2.5-flash-preview-05-20"

    response = client.models.generate_content(
        model=model_id,
        contents=[
            Part.from_uri(
                file_uri="https://www.youtube.com/watch?v=3KtWfp0UopM",
                mime_type="video/mp4",
            ),
            "Write a short and engaging blog post based on this video.",
        ],
    )

    print(response.text)
    # Example response:
    # Here's a short blog post based on the video provided:
    #
    # **Google Turns 25: A Quarter Century of Search!**
    # ...

    # [END googlegenaisdk_textgen_with_youtube_video]
    return response.text


if __name__ == "__main__":
    generate_content()
