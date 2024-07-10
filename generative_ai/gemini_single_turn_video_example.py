# Copyright 2023 Google LLC
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


def generate_text(project_id: str) -> str:
    # [START generativeaionvertexai_gemini_single_turn_video]
    import vertexai

    from vertexai.generative_models import GenerativeModel, Part

    # TODO(developer): Update and un-comment below line
    # project_id = "PROJECT_ID"

    vertexai.init(project=project_id, location="us-central1")

    vision_model = GenerativeModel("gemini-1.5-flash-001")

    # Generate text
    response = vision_model.generate_content(
        [
            Part.from_uri(
                "gs://cloud-samples-data/video/animals.mp4", mime_type="video/mp4"
            ),
            "What is in the video?",
        ]
    )
    print(response.text)
    # [END generativeaionvertexai_gemini_single_turn_video]

    return response.text
