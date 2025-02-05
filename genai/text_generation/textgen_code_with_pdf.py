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
    # [START googlegenaisdk_textgen_code_with_pdf]
    from google import genai
    from google.genai import types

    client = genai.Client()
    model_id = "gemini-2.0-flash-exp"

    python_code = types.Part.from_uri(
        file_uri="https://storage.googleapis.com/cloud-samples-data/generative-ai/text/inefficient_fibonacci_series_python_code.pdf",
        mime_type="application/pdf",
    )

    response = client.models.generate_content(
        model=model_id,
        contents=[
            python_code,
            "Convert this python code to use Google Python Style Guide.",
        ],
    )

    print(response.text)
    # Example response:
    # ```python
    # def fibonacci(n: int) -> list[int] | str:
    # ...
    # [END googlegenaisdk_textgen_code_with_pdf]
    return response.text


if __name__ == "__main__":
    generate_content()
