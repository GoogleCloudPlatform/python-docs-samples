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


def generate_content() -> None:
    # [START generativeaionvertexai_gemini_express_mode]
    import vertexai
    from vertexai.generative_models import GenerativeModel

    # TODO(developer): Update below line
    vertexai.init(api_key="YOUR_API_KEY")

    model = GenerativeModel("gemini-1.5-flash")

    response = model.generate_content("Explain bubble sort to me")

    print(response.text)
    # Example response:
    # Bubble Sort is a simple sorting algorithm that repeatedly steps through the list
    # [END generativeaionvertexai_gemini_express_mode]
    return response.text
