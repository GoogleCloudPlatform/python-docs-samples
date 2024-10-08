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


def generate_content() -> object:
    # [START generativeaionvertexai_non_stream_multimodality_basic]
    import vertexai

    from vertexai.generative_models import GenerativeModel, Part

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"

    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-002")
    response = model.generate_content(
        [
            Part.from_uri(
                "gs://cloud-samples-data/generative-ai/video/animals.mp4", "video/mp4"
            ),
            Part.from_uri(
                "gs://cloud-samples-data/generative-ai/image/character.jpg",
                "image/jpeg",
            ),
            "Are these video and image correlated?",
        ]
    )

    print(response.text)
    # Example response:
    # No, the video and image are not correlated.
    # The video shows a Google Photos project where animals at the
    # Los Angeles Zoo take selfies using a specially designed camera rig.
    # The image is a simple drawing of a wizard.

    # [END generativeaionvertexai_non_stream_multimodality_basic]
    return response


if __name__ == "__main__":
    generate_content()
