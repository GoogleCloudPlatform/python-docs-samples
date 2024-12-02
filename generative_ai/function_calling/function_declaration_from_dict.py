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

from vertexai.generative_models import FunctionDeclaration


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def function_declaration_from_dict() -> object:
    # [START generativeaionvertexai_gemini_function_calling_declare_from_dict1]
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
    # [END generativeaionvertexai_gemini_function_calling_declare_from_dict1]
    # [START generativeaionvertexai_gemini_function_calling_declare_from_dict2]
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
    # [END generativeaionvertexai_gemini_function_calling_declare_from_dict2]
    return [get_current_weather_func, extract_sale_records_func]


if __name__ == "__main__":
    function_declaration_from_dict()
