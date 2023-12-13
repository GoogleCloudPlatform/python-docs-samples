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

# [START aiplatform_gemini_guide_step1]
# TODO(developer): Vertex AI SDK - uncomment below & run
# pip3 install --upgrade --user google-cloud-aiplatform
# gcloud auth application-default login
# [END aiplatform_gemini_guide_step1]


def generate_text(project_id, location):
    # [START aiplatform_gemini_guide_step2]
    # Initialize Vertex AI
    import vertexai

    # TODO(developer): Update and un-comment below line
    # project_id = "PROJECT_ID"
    location = "us-central1"

    vertexai.init(project=project_id, location=location)
    # [END aiplatform_gemini_guide_step2]

    # [START aiplatform_gemini_guide_step3]
    from vertexai.preview.generative_models import GenerativeModel, Part

    # [END aiplatform_gemini_guide_step3]

    # [START aiplatform_gemini_guide_step4]
    multimodal_model = GenerativeModel("gemini-pro-vision")
    # [END aiplatform_gemini_guide_step4]

    # [START aiplatform_gemini_guide_step5]
    response = multimodal_model.generate_content(
        [
            "what is shown in this image?",
            Part.from_uri(
                "gs://generativeai-downloads/images/scones.jpg", mime_type="image/jpeg"
            ),
        ]
    )
    print(response)
    # [END aiplatform_gemini_guide_step5]
    return response.text
