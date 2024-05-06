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

def generate_content(PROJECT_ID: str, REGION: str, MODEL_ID: str):
    # [START generativeaionvertexai_count_tokens_advanced] 
    import vertexai
    from vertexai.generative_models import GenerativeModel, Part

    vertexai.init(project=PROJECT_ID, location=REGION)

    contents = [
        Part.from_uri(
            "gs://cloud-samples-data/generative-ai/video/pixel8.mp4", mime_type="video/mp4"
        ),
        "Provide a description of the video.",
    ]

    gemini_model = GenerativeModel(MODEL_ID)
    model_response = gemini_model.count_tokens(contents)

    print(model_response)
    # [END generativeaionvertexai_count_tokens_advanced]
    return model_response