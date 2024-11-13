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
    # [START generativeaionvertexai_stream_text_basic]
    import vertexai

    from vertexai.generative_models import GenerativeModel

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-002")
    responses = model.generate_content(
        "Write a story about a magic backpack.", stream=True
    )

    for response in responses:
        print(response.text)
    # Example response:
    # El
    # ara wasn't looking for magic. She was looking for rent money.
    # Her tiny apartment, perched precariously on the edge of Whispering Woods,
    # ...

    # [END generativeaionvertexai_stream_text_basic]
    return responses


if __name__ == "__main__":
    generate_content()
