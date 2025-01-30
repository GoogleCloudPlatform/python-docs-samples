#!/bin/zsh

# Example usage:
# generate_python_file example.py


filename="$1"

# Validate input
if [[ -z "$filename" ]]; then
    echo "Error: No filename provided"
    echo "Usage: generate_python_file filename.py"
    exit 1
fi

# Check file extension
if [[ ! "$filename" =~ \.py$ ]]; then
    echo "Error: Filename must have .py extension"
    exit 1
fi

# Extract directory path if it exists
dirpath=$(dirname "$filename")

# Create directory if it doesn't exist
if [[ "$dirpath" != "." ]]; then
    if ! mkdir -p "$dirpath"; then
        echo "Error: Failed to create directory: $dirpath"
        exit 1
    fi
    echo "Created directory: $dirpath"
fi

# Check if file already exists
if [[ -f "$filename" ]]; then
    echo "Error: File $filename already exists"
    exit 1
fi

# Extract filename without extension for region tags
basename="${filename%.py}"
# Remove any leading ./ from basename
basename="${basename#./}"

# Generate file content
cat > "$filename" << EOL
# Copyright 2025 Google LLC
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


def generate_content() -> str:
    # [START googlegenaisdk_${basename}]
    from google import genai

    # [END googlegenaisdk_${basename}]
    return response.text


if __name__ == "__main__":
    generate_content()
EOL

echo "Created Python file: $filename"
exit 0

