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


def count_tokens() -> int:
    # [START googlegenaisdk_counttoken_with_txt_vid]
    from google import genai
    from google.genai.types import HttpOptions, Part

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    contents = [
        Part.from_uri(
            file_uri="gs://cloud-samples-data/generative-ai/video/pixel8.mp4",
            mime_type="video/mp4",
        ),
        "Provide a description of the video.",
    ]

    response = client.models.count_tokens(
        model="gemini-2.5-flash-preview-05-20",
        contents=contents,
    )
    print(response)
    # Example output:
    # total_tokens=16252 cached_content_token_count=None
    # [END googlegenaisdk_counttoken_with_txt_vid]
    return response.total_tokens


if __name__ == "__main__":
    count_tokens()
