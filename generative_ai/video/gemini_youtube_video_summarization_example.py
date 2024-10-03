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


def generate_content() -> str:
    # [START generativeaionvertexai_gemini_youtube_video_summarization]
    import vertexai
    from vertexai.generative_models import GenerativeModel, Part

    # TODO (developer): update project id
    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-002")

    contents = [
        # Text prompt
        "Summarize this video.",
        # YouTube video of Google Pixel 9
        Part.from_uri("https://youtu.be/sXrasaDZxw0", "video/mp4"),
    ]

    response = model.generate_content(contents)
    print(response.text)
    # Example response:
    #     'This Google Pixel 9 Pro advertisement shows how the Gemini AI feature enhances'
    #     ' the capabilities of the phone. The video starts with ...'
    # [END generativeaionvertexai_gemini_youtube_video_summarization]
    return response.text


if __name__ == "__main__":
    generate_content()
