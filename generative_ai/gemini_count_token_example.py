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


from vertexai.generative_models import GenerationResponse


def count_tokens(project_id: str) -> GenerationResponse:
    # [START generativeaionvertexai_gemini_token_count]
    import vertexai
    from vertexai.generative_models import GenerativeModel

    # TODO(developer): Update and un-comment below line
    # project_id = "PROJECT_ID"

    vertexai.init(project=project_id, location="us-central1")

    model = GenerativeModel(model_name="gemini-1.0-pro-002")

    prompt = "Why is the sky blue?"

    # Prompt tokens count
    response = model.count_tokens(prompt)
    usage_metadata = response.usage_metadata
    print(f"Prompt Token Count: {usage_metadata.prompt_token_count}")

    # Send text to Gemini
    response = model.generate_content(prompt)

    # Response tokens count
    usage_metadata = response.usage_metadata
    print(f"Prompt Token Count: {usage_metadata.prompt_token_count}")
    print(f"Candidates Token Count: {usage_metadata.candidates_token_count}")
    print(f"Total Token Count: {usage_metadata.total_token_count}")

    # [END generativeaionvertexai_gemini_token_count]
    return response


def count_tokens_multimodal(project_id: str) -> GenerationResponse:
    # [START generativeaionvertexai_gemini_token_count_multimodal]
    import vertexai
    from vertexai.generative_models import GenerativeModel, Part

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"

    vertexai.init(project=project_id, location="us-central1")

    model = GenerativeModel(model_name="gemini-1.0-pro-002")

    contents = [
        Part.from_uri(
            "gs://cloud-samples-data/generative-ai/video/pixel8.mp4",
            mime_type="video/mp4",
        ),
        "Provide a description of the video.",
    ]

    # Prompt tokens count
    response = model.count_tokens(contents)
    usage_metadata = response.usage_metadata
    print(f"Prompt Token Count: {usage_metadata.prompt_token_count}")

    # Send text to Gemini
    response = model.generate_content(contents)
    usage_metadata = response.usage_metadata

    # Response tokens count
    print(f"Prompt Token Count: {usage_metadata.prompt_token_count}")
    print(f"Candidates Token Count: {usage_metadata.candidates_token_count}")
    print(f"Total Token Count: {usage_metadata.total_token_count}")

    # [END generativeaionvertexai_gemini_token_count_multimodal]
    return response
