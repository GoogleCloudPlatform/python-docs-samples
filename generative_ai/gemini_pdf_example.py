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


def analyze_pdf(project_id: str) -> str:
    # [START generativeaionvertexai_gemini_pdf]

    import vertexai
    from vertexai.generative_models import GenerativeModel, Part

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"

    vertexai.init(project=project_id, location="us-central1")

    model = GenerativeModel("gemini-1.5-pro-preview-0409")

    prompt = """
    Your are a very professional document summarization specialist.
    Please summarize the given document.
    """

    pdf_file_uri = "gs://cloud-samples-data/generative-ai/pdf/2403.05530.pdf"
    pdf_file = Part.from_uri(pdf_file_uri, mime_type="application/pdf")
    contents = [pdf_file, prompt]

    response = model.generate_content(contents)
    print(response.text)

    # [END generativeaionvertexai_gemini_pdf]
    return response.text
