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

from typing import List

from vertexai.generative_models import FunctionDeclaration


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def prototype():
    # [START TBD]
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
    # [END TBD]
    return multiply_number_func


if __name__ == "__main__":
    prototype()
