# Copyright 2025 Google LLC
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
    # [START googlegenaisdk_textgen_code_with_pdf]
    from google import genai
    from google.genai.types import HttpOptions, Part

    client = genai.Client(http_options=HttpOptions(api_version="v1beta1"))
    model_id = "gemini-2.5-flash"
    prompt = "Convert this python code to use Google Python Style Guide."
    print("> ", prompt, "\n")
    pdf_uri = "https://storage.googleapis.com/cloud-samples-data/generative-ai/text/inefficient_fibonacci_series_python_code.pdf"

    pdf_file = Part.from_uri(
        file_uri=pdf_uri,
        mime_type="application/pdf",
    )

    response = client.models.generate_content(
        model=model_id,
        contents=[pdf_file, prompt],
    )

    print(response.text)
    # Example response:
    # >  Convert this python code to use Google Python Style Guide.
    #
    # def generate_fibonacci_sequence(num_terms: int) -> list[int]:
    #     """Generates the Fibonacci sequence up to a specified number of terms.
    #
    #     This function calculates the Fibonacci sequence starting with 0 and 1.
    #     It handles base cases for 0, 1, and 2 terms efficiently.
    #
    # # ...
    # [END googlegenaisdk_textgen_code_with_pdf]
    return response.text


if __name__ == "__main__":
    generate_content()
