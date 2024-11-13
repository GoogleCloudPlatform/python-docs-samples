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


def analyze_pdf() -> str:
    # [START generativeaionvertexai_gemini_pdf]
    import vertexai

    from vertexai.generative_models import GenerativeModel, Part

    # TODO(developer): Update project_id and location
    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-002")

    prompt = """
    You are a very professional document summarization specialist.
    Please summarize the given document.
    """

    pdf_file = Part.from_uri(
        uri="gs://cloud-samples-data/generative-ai/pdf/2403.05530.pdf",
        mime_type="application/pdf",
    )
    contents = [pdf_file, prompt]

    response = model.generate_content(contents)
    print(response.text)
    # Example response:
    # Here's a summary of the provided text, which appears to be a research paper on the Gemini 1.5 Pro
    # multimodal large language model:
    # **Gemini 1.5 Pro: Key Advancements and Capabilities**
    # The paper introduces Gemini 1.5 Pro, a highly compute-efficient multimodal model
    # significantly advancing long-context capabilities
    # ...

    # [END generativeaionvertexai_gemini_pdf]
    return response.text


if __name__ == "__main__":
    analyze_pdf()
