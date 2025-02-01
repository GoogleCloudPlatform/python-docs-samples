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


def create_app() -> object:
    # [START generativeaionvertexai_gemini_function_calling_app_setup]
    from typing import List

    import vertexai

    from vertexai.generative_models import (
        Content,
        FunctionDeclaration,
        GenerationConfig,
        GenerativeModel,
        Part,
        Tool,
        ToolConfig,
    )

    # Initialize Vertex AI
    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = 'your-project-id'
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # Initialize Gemini model
    model = GenerativeModel(model_name="gemini-1.5-flash-002")
    # [END generativeaionvertexai_gemini_function_calling_app_setup]

    # [START generativeaionvertexai_gemini_function_calling_app_declare_1]
    function_name = "get_current_weather"
    get_current_weather_func = FunctionDeclaration(
        name=function_name,
        description="Get the current weather in a given location",
        # Function parameters are specified in JSON schema format
        parameters={
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "The city name of the location for which to get the weather."}
            },
        },
    )
    # [END generativeaionvertexai_gemini_function_calling_app_declare_1]

    # [START generativeaionvertexai_gemini_function_calling_app_declare_2]
    extract_sale_records_func = FunctionDeclaration(
        name="extract_sale_records",
        description="Extract sale records from a document.",
        parameters={
            "type": "object",
            "properties": {
                "records": {
                    "type": "array",
                    "description": "A list of sale records",
                    "items": {
                        "description": "Data for a sale record",
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer", "description": "The unique id of the sale."},
                            "date": {"type": "string", "description": "Date of the sale, in the format of MMDDYY, e.g., 031023"},
                            "total_amount": {"type": "number", "description": "The total amount of the sale."},
                            "customer_name": {"type": "string", "description": "The name of the customer, including first name and last name."},
                            "customer_contact": {"type": "string", "description": "The phone number of the customer, e.g., 650-123-4567."},
                        },
                        "required": ["id", "date", "total_amount"],
                    },
                },
            },
            "required": ["records"],
        },
    )
    # [END generativeaionvertexai_gemini_function_calling_app_declare_2]

    # [START generativeaionvertexai_gemini_function_calling_app_declare_3]
    # Define a function. Could be a local function or you can import the requests library to call an API
    def multiply_numbers(numbers: List[int]) -> int:
        """
        Calculates the product of all numbers in an array.

        Args:
            numbers: An array of numbers to be multiplied.

        Returns:
            The product of all the numbers. If the array is empty, returns 1.
        """

        if not numbers:  # Handle empty array
            return 1

        product = 1
        for num in numbers:
            product *= num

        return product

    multiply_number_func = FunctionDeclaration.from_func(multiply_numbers)

    '''
    multiply_number_func contains the following schema:

    name: "multiply_numbers"
    description: "Calculates the product of all numbers in an array."
    parameters {
      type_: OBJECT
      properties {
        key: "numbers"
        value {
          description: "An array of numbers to be multiplied."
          title: "Numbers"
        }
      }
      required: "numbers"
      description: "Calculates the product of all numbers in an array."
      title: "multiply_numbers"
    }
    '''
    # [END generativeaionvertexai_gemini_function_calling_app_declare_3]

    # [START generativeaionvertexai_gemini_function_calling_app_prompt]
    # Define the user's prompt in a Content object that we can reuse in model calls
    user_prompt_content = Content(
        role="user",
        parts=[
            Part.from_text("What is the weather like in Boston?"),
        ],
    )
    # [END generativeaionvertexai_gemini_function_calling_app_prompt]

    # [START generativeaionvertexai_gemini_function_calling_app_submit]
    # Define a tool that includes some of the functions that we declared earlier
    tool = Tool(
        function_declarations=[get_current_weather_func, extract_sale_records_func, multiply_number_func],
    )

    # Send the prompt and instruct the model to generate content using the Tool object that you just created
    response = model.generate_content(
        user_prompt_content,
        generation_config=GenerationConfig(temperature=0),
        tools=[tool],
        tool_config=ToolConfig(
            function_calling_config=ToolConfig.FunctionCallingConfig(
                # ANY mode forces the model to predict only function calls
                mode=ToolConfig.FunctionCallingConfig.Mode.ANY,
                # Allowed function calls to predict when the mode is ANY. If empty, any  of
                # the provided function calls will be predicted.
                allowed_function_names=["get_current_weather"],
            )
        )
    )
    # [END generativeaionvertexai_gemini_function_calling_app_submit]

    # flake8: noqa=F841 # Intentionally unused variable `location` in sample code
    # [START generativeaionvertexai_gemini_function_calling_app_invoke]
    # Check the function name that the model responded with, and make an API call to an external system
    if (response.candidates[0].function_calls[0].name == "get_current_weather"):
        # Extract the arguments to use in your API call
        location = response.candidates[0].function_calls[0].args["location"]

        # Here you can use your preferred method to make an API request to fetch the current weather, for example:
        # api_response = requests.post(weather_api_url, data={"location": location})

        # In this example, we'll use synthetic data to simulate a response payload from an external API
        api_response = """{ "location": "Boston, MA", "temperature": 38, "description": "Partly Cloudy",
                        "icon": "partly-cloudy", "humidity": 65, "wind": { "speed": 10, "direction": "NW" } }"""
    # [END generativeaionvertexai_gemini_function_calling_app_invoke]
    # flake8: qa=F841

    # [START generativeaionvertexai_gemini_function_calling_app_generate]
    response = model.generate_content(
        [
            user_prompt_content,  # User prompt
            response.candidates[0].content,  # Function call response
            Content(
                parts=[
                    Part.from_function_response(
                        name="get_current_weather",
                        response={
                            "content": api_response,  # Return the API response to Gemini
                        },
                    )
                ],
            ),
        ],
        tools=[tool],
    )
    # Get the model summary response
    summary = response.text
    # [END generativeaionvertexai_gemini_function_calling_app_generate]

    return { "weather_response": summary, "tool": tool }


if __name__ == "__main__":
    create_app()
