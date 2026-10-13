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


def generate_content() -> str:
    # [START googlegenaisdk_interactions_textgen_with_pdf]
    from google import genai
    from google.genai.interactions import DocumentContent, TextContent

    client = genai.Client()
    model_id = "gemini-3.8-flash"

    prompt = """
    You are a highly skilled document summarization specialist.
    Your task is to provide a concise executive summary of no more than 300 words.
    Please summarize the given document for a general audience.
    """

    interaction = client.interactions.create(
        model=model_id,
        input=[
            DocumentContent(
                uri="gs://cloud-samples-data/generative-ai/pdf/1706.03762v7.pdf",
                mime_type="application/pdf",
            ),
            TextContent(text=prompt),
        ],
    )

    print(interaction.output_text)
    # Example response:
    # Here is a summary of the document in 300 words.
    #
    # The paper introduces the Transformer, a novel neural network architecture for
    # sequence transduction tasks like machine translation. Unlike existing models that rely on recurrent or
    # convolutional layers, the Transformer is based entirely on attention mechanisms.
    # ...
    # [END googlegenaisdk_interactions_textgen_with_pdf]
    return interaction.output_text


if __name__ == "__main__":
    generate_content()
