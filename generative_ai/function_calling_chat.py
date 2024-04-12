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

# [START generativeaionvertexai_gemini_function_calling_chat]
import vertexai
from vertexai.generative_models import (
    FunctionDeclaration,
    GenerativeModel,
    Part,
    Tool,
)


def generate_function_call_chat(project_id: str, location: str) -> tuple:
    prompts = []
    summaries = []

    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    # Specify a function declaration and parameters for an API request
    get_product_info_func = FunctionDeclaration(
        name="get_product_sku",
        description="Get the SKU for a product",
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

    # Initialize Gemini model
    model = GenerativeModel(
        "gemini-1.0-pro", generation_config={"temperature": 0}, tools=[retail_tool]
    )

    # Start a chat session
    chat = model.start_chat()

    # Send a prompt for the first conversation turn that should invoke the get_product_sku function
    prompt = "Do you have the Pixel 8 Pro in stock?"
    response = chat.send_message(prompt)
    prompts.append(prompt)

    # Check the function name that the model responded with, and make an API call to an external system
    if response.candidates[0].content.parts[0].function_call.name == "get_product_sku":
        # Extract the arguments to use in your API call
        product_name = (
            response.candidates[0].content.parts[0].function_call.args["product_name"]
        )
        product_name

        # Here you can use your preferred method to make an API request to retrieve the product SKU, as in:
        # api_response = requests.post(product_api_url, data={"product_name": product_name})

        # In this example, we'll use synthetic data to simulate a response payload from an external API
        api_response = {"sku": "GA04834-US", "in_stock": "yes"}

    # Return the API response to Gemini so it can generate a model response or request another function call
    response = chat.send_message(
        Part.from_function_response(
            name="get_product_sku",
            response={
                "content": api_response,
            },
        ),
    )

    # Extract the text from the summary response
    summary = response.candidates[0].content.parts[0].text
    summaries.append(summary)

    # Send a prompt for the second conversation turn that should invoke the get_store_location function
    prompt = "Is there a store in Mountain View, CA that I can visit to try it out?"
    response = chat.send_message(prompt)
    prompts.append(prompt)

    # Check the function name that the model responded with, and make an API call to an external system
    if (
        response.candidates[0].content.parts[0].function_call.name
        == "get_store_location"
    ):
        # Extract the arguments to use in your API call
        location = (
            response.candidates[0].content.parts[0].function_call.args["location"]
        )
        location

        # Here you can use your preferred method to make an API request to retrieve store location closest to the user, as in:
        # api_response = requests.post(store_api_url, data={"location": location})

        # In this example, we'll use synthetic data to simulate a response payload from an external API
        api_response = {"store": "2000 N Shoreline Blvd, Mountain View, CA 94043, US"}

    # Return the API response to Gemini so it can generate a model response or request another function call
    response = chat.send_message(
        Part.from_function_response(
            name="get_store_location",
            response={
                "content": api_response,
            },
        ),
    )

    # Extract the text from the summary response
    summary = response.candidates[0].content.parts[0].text
    summaries.append(summary)

    return prompts, summaries


# [END generativeaionvertexai_gemini_function_calling_chat]
