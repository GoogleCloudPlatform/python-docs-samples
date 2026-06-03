# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# test_pass.py


def calculate_square(number: int) -> int:
    """Calculates the square of a given integer."""
    result = number * number
    print(f"The result is: {result}")
    return result


if __name__ == "__main__":
    # Ensure a basic execution works cleanly
    calculate_square(5)
