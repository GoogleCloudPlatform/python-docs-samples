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


def generate_from_text_input(project_id: str) -> str:
    # [START generativeaionvertexai_gemini_generate_from_text_input]
    import vertexai
    from vertexai.generative_models import GenerativeModel, Part

    # TODO(developer): Update and un-comment below line
    # project_id = "PROJECT_ID"

    vertexai.init(project=project_id, location="us-central1")

    model = GenerativeModel(model_name="gemini-1.0-pro-002")

    response = model.generate_content(
        [
            # Does the returned sentiment score match the reviewer's movie rating?
            Part.from_text(
                """Give a score from 1 - 10 to suggest if the
                following movie review is negative or positive (1 is most
                negative, 10 is most positive, 5 will be neutral). Include an
                explanation.

                The movie takes some time to build, but that is part of its beauty.
                By the time you are hooked, this tale of friendship and hope is
                thrilling and affecting, until the very last scene. You will find
                yourself rooting for the hero every step of the way. This is the
                sharpest, most original animated film I have seen in years.
                I would give it 8 out of 10 stars."""
            )
        ]
    )

    print(response.text)
    # [END generativeaionvertexai_gemini_generate_from_text_input]

    return response.text
