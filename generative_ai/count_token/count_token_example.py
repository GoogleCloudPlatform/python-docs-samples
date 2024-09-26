# Copyright 2023 Google LLC
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


def count_token_locally() -> int:
    # [START generativeaionvertexai_token_count_sample_with_local_sdk]
    from vertexai.preview.tokenization import get_tokenizer_for_model
    from vertexai.generative_models import FunctionDeclaration, Tool

    # init local tokenzier
    tokenizer = get_tokenizer_for_model("gemini-1.5-flash-001")

    # simple text
    prompt = "hello world"
    response = tokenizer.count_tokens(prompt)
    print(f"Prompt Token Count: {response.total_tokens}")
    # Example response:
    #   Prompt Token Count: 2

    # simple text with system instructions
    prompt = ["hello world", "what's the weather today"]
    response = tokenizer.count_tokens(prompt, system_instruction="you are a chatbot")
    print(f"Prompt Token Count: {response.total_tokens}")
    # Example response:
    #   Prompt Token Count: 12

    # Count tokens with a function declaration
    def get_current_weather(location: str, unit: str = "centigrade") -> dict:
        """Gets weather in the specified location.
        Args:
            location: The location for which to get the weather.
            unit: Optional. Temperature unit. Can be Centigrade or Fahrenheit. Defaults to Centigrade.
        Returns:
            The weather information as a dict.
        """
        return dict(
            location="us-central1",
            unit=unit,
            weather="Super nice, but maybe a bit hot.",
        )

    weather_tool = Tool(
        function_declarations=[FunctionDeclaration.from_func(get_current_weather)]
    )
    print(tokenizer.count_tokens("hello", tools=[weather_tool]))
    # Example response:
    #     CountTokensResult(total_tokens=49)
    # [END generativeaionvertexai_token_count_sample_with_local_sdk]
    return response.total_tokens


# TODO: Delete the following samples after API deprecation. `count_token_locally` is faster & recommended.
def count_token_service() -> int:
    # [START generativeaionvertexai_token_count_sample_with_genai]
    import vertexai
    from vertexai.generative_models import GenerativeModel

    # TODO(developer): Update project & location
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # using Vertex AI Model as tokenzier
    model = GenerativeModel("gemini-1.5-flash-002")

    prompt = "hello world"
    response = model.count_tokens(prompt)
    print(f"Prompt Token Count: {response.total_tokens}")
    print(f"Prompt Character Count: {response.total_billable_characters}")
    # Example response:
    #     Prompt Token Count: 2
    #     Prompt Token Count: 10

    prompt = ["hello world", "what's the weather today"]
    response = model.count_tokens(prompt)
    print(f"Prompt Token Count: {response.total_tokens}")
    print(f"Prompt Character Count: {response.total_billable_characters}")
    # Example response:
    #     Prompt Token Count: 8
    #     Prompt Token Count: 31
    # [END generativeaionvertexai_token_count_sample_with_genai]
    return response.total_tokens


if __name__ == "__main__":
    count_token_locally()
    count_token_service()
