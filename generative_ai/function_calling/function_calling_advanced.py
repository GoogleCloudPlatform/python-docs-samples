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


def generate_content(PROJECT_ID: str, REGION: str, MODEL_ID: str) -> object:
    # [START generativeaionvertexai_function_calling_advanced]
    import vertexai
    from vertexai.generative_models import (
        FunctionDeclaration,
        GenerativeModel,
        GenerationConfig,
        Part,
        Tool,
        ToolConfig,
    )

    vertexai.init(project=PROJECT_ID, location=REGION)

    # Specify a function declaration and parameters for an API request
    get_product_info_func = FunctionDeclaration(
        name="get_product_sku",
        description="Get the available inventory for a Google products, e.g: Pixel phones, Pixel Watches, Google Home etc",
        # Function parameters are specified in OpenAPI JSON schema format
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
        # Function parameters are specified in OpenAPI JSON schema format
        parameters={
            "type": "object",
            "properties": {"location": {"type": "string", "description": "Location"}},
        },
    )

    # Define a tool that includes the above functions
    retail_tool = Tool(
        function_declarations=[
            get_product_info_func,
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

    generation_config = GenerationConfig(
        temperature=0.95, top_p=1.0, max_output_tokens=8192
    )

    model = GenerativeModel(
        MODEL_ID,
        generation_config=generation_config,
        tools=[retail_tool],
        tool_config=retail_tool_config,
    )
    response = model.generate_content(
        "Do you have the White Pixel 8 Pro 128GB in stock in the US?"
    )

    print(response)
    # [END generativeaionvertexai_function_calling_advanced]

    return response