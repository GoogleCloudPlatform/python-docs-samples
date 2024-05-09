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

from vertexai.generative_models import GenerationResponse


def generate_function_call(project_id: str) -> GenerationResponse:
    # [START generativeaionvertexai_gemini_function_calling]
    import vertexai
    from vertexai.generative_models import (
        Content,
        FunctionDeclaration,
        GenerationConfig,
        GenerativeModel,
        Part,
        Tool,
    )

    # Initialize Vertex AI
    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    vertexai.init(project=project_id)

    # Initialize Gemini model
    model = GenerativeModel(model_name="gemini-1.0-pro-001")

    # Define the user's prompt in a Content object that we can reuse in model calls
    user_prompt_content = Content(
        role="user",
        parts=[
            Part.from_text("What is the weather like in Boston?"),
        ],
    )

    # Specify a function declaration and parameters for an API request
    function_name = "get_current_weather"
    get_current_weather_func = FunctionDeclaration(
        name=function_name,
        description="Get the current weather in a given location",
        # Function parameters are specified in OpenAPI JSON schema format
        parameters={
            "type": "object",
            "properties": {"location": {"type": "string", "description": "Location"}},
        },
    )

    # Define a tool that includes the above get_current_weather_func
    weather_tool = Tool(
        function_declarations=[get_current_weather_func],
    )

    # Send the prompt and instruct the model to generate content using the Tool that you just created
    response = model.generate_content(
        user_prompt_content,
        generation_config=GenerationConfig(temperature=0),
        tools=[weather_tool],
    )
    function_call = response.candidates[0].function_calls[0]
    print(function_call)

    # Check the function name that the model responded with, and make an API call to an external system
    if function_call.name == function_name:
        # Extract the arguments to use in your API call
        location = function_call.args["location"]  # noqa: F841

        # Here you can use your preferred method to make an API request to fetch the current weather, for example:
        # api_response = requests.post(weather_api_url, data={"location": location})

        # In this example, we'll use synthetic data to simulate a response payload from an external API
        api_response = """{ "location": "Boston, MA", "temperature": 38, "description": "Partly Cloudy",
                        "icon": "partly-cloudy", "humidity": 65, "wind": { "speed": 10, "direction": "NW" } }"""

    # Return the API response to Gemini so it can generate a model response or request another function call
    response = model.generate_content(
        [
            user_prompt_content,  # User prompt
            response.candidates[0].content,  # Function call response
            Content(
                parts=[
                    Part.from_function_response(
                        name=function_name,
                        response={
                            "content": api_response,  # Return the API response to Gemini
                        },
                    ),
                ],
            ),
        ],
        tools=[weather_tool],
    )

    # Get the model response
    print(response.text)
    # [END generativeaionvertexai_gemini_function_calling]
    return response


def generate_function_call_advanced(project_id: str) -> GenerationResponse:
    # [START generativeaionvertexai_gemini_function_calling_advanced]
    import vertexai
    from vertexai.preview.generative_models import (
        FunctionDeclaration,
        GenerativeModel,
        Tool,
        ToolConfig,
    )

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"

    # Initialize Vertex AI
    vertexai.init(project=project_id)

    # Specify a function declaration and parameters for an API request
    get_product_sku_func = FunctionDeclaration(
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
        "gemini-1.5-pro-preview-0409",
        tools=[retail_tool],
        tool_config=retail_tool_config,
    )
    response = model.generate_content(
        "Do you have the Pixel 8 Pro 128GB in stock?",
    )

    print(response.text)
    print(response.candidates[0].function_calls)
    # [END generativeaionvertexai_gemini_function_calling_advanced]
    return response
