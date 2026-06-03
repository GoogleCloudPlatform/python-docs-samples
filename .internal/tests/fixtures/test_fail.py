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

# test_fail.py
import sys  # Flake8 Error: 'sys' imported but unused
import os

def calculate_square (number): # Flake8 Error: extra space before opening parenthesis
    
    result=number*number # Flake8 Error: missing whitespace around operator '='
    print('The result is: ' + str(result)) # Black will want to change single quotes to double quotes
    return result 

# Intentional trailing whitespace on the line below to trigger Flake8
