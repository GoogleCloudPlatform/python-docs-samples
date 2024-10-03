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


def generate_content() -> object:
    # [START generativeaionvertexai_non_stream_text_basic]
    import vertexai

    from vertexai.generative_models import GenerativeModel

    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-002")
    response = model.generate_content("Write a story about a magic backpack.")

    print(response.text)
    # [END generativeaionvertexai_non_stream_text_basic]

    return response


if __name__ == "__main__":
    generate_content()
