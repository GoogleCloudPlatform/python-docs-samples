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


def analyze_video_with_audio() -> str:
    # [START generativeaionvertexai_gemini_video_with_audio]

    import vertexai
    from vertexai.generative_models import GenerativeModel, Part

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"

    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-002")

    prompt = """
    Provide a description of the video.
    The description should also contain anything important which people say in the video.
    """

    video_file = Part.from_uri(
        uri="gs://cloud-samples-data/generative-ai/video/pixel8.mp4",
        mime_type="video/mp4",
    )

    contents = [video_file, prompt]

    response = model.generate_content(contents)
    print(response.text)
    # Example response:
    # Here is a description of the video.
    # ... Then, the scene changes to a woman named Saeko Shimada..
    # She says, "Tokyo has many faces. The city at night is totally different
    # from what you see during the day."
    # ...

    # [END generativeaionvertexai_gemini_video_with_audio]
    return response.text


if __name__ == "__main__":
    analyze_video_with_audio()
