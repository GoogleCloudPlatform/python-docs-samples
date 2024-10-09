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

from vertexai.generative_models import GenerationResponse

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def generate_function_call_advanced() -> GenerationResponse:
    # [START generativeaionvertexai_gemini_function_calling_advanced]
    import vertexai

    from vertexai.preview.generative_models import (
        FunctionDeclaration,
        GenerativeModel,
        Tool,
        ToolConfig,
    )

    # TODO(developer): Update & uncomment below line
    # PROJECT_ID = "your-project-id"

    # Initialize Vertex AI
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # Specify a function declaration and parameters for an API request
    get_product_sku_func = FunctionDeclaration(
        name="get_product_sku",
        description="Get the available inventory for a Google products, e.g: Pixel phones, Pixel Watches, Google Home etc",
        # Function parameters are specified in JSON schema format
        parameters={
            "type": "object",
            "properties": {
                "product_name": {"type": "string", "description": "Product name"}
            },
        },
    )

    # Specify another function declaration and parameters for an API request
    get_store_location_func = FunctionDeclaration(
        name="get_store_location",
        description="Get the location of the closest store",
        # Function parameters are specified in JSON schema format
        parameters={
            "type": "object",
            "properties": {"location": {"type": "string", "description": "Location"}},
        },
    )

    # Define a tool that includes the above functions
    retail_tool = Tool(
        function_declarations=[
            get_product_sku_func,
            get_store_location_func,
        ],
    )

    # Define a tool config for the above functions
    retail_tool_config = ToolConfig(
        function_calling_config=ToolConfig.FunctionCallingConfig(
            # ANY mode forces the model to predict a function call
            mode=ToolConfig.FunctionCallingConfig.Mode.ANY,
            # List of functions that can be returned when the mode is ANY.
            # If the list is empty, any declared function can be returned.
            allowed_function_names=["get_product_sku"],
        )
    )

    model = GenerativeModel(
        model_name="gemini-1.5-flash-002",
        tools=[retail_tool],
        tool_config=retail_tool_config,
    )
    response = model.generate_content(
        "Do you have the Pixel 8 Pro 128GB in stock?",
    )

    print(response.candidates[0].function_calls)
    # Example response:
    # [
    # name: "get_product_sku"
    # args {
    #   fields { key: "product_name" value { string_value: "Pixel 8 Pro 128GB" }}
    #   }
    # ]

    # [END generativeaionvertexai_gemini_function_calling_advanced]
    return response


if __name__ == "__main__":
    generate_function_call_advanced()
