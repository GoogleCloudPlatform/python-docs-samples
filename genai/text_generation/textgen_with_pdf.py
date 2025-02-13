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
    # [START googlegenaisdk_textgen_with_pdf]
    from google import genai
    from google.genai.types import HttpOptions, Part

    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    model_id = "gemini-2.0-flash-001"

    prompt = """
    You are a highly skilled document summarization specialist. Your task is to provide a concise executive summary of no more than 300 words. Please summarize the given document for a general audience.
    """

    pdf_file = Part.from_uri(
        file_uri="gs://cloud-samples-data/generative-ai/pdf/2403.05530.pdf",
        mime_type="application/pdf",
    )

    response = client.models.generate_content(
        model=model_id,
        contents=[pdf_file, prompt],
    )

    print(response.text)
    # Example response:
    # Here's a summary of the Google DeepMind Gemini 1.5 report:
    #
    # This report introduces Gemini 1.5 Pro...
    # [END googlegenaisdk_textgen_with_pdf]
    return response.text


if __name__ == "__main__":
    generate_content()
