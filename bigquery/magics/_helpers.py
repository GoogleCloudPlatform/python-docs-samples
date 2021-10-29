# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def strip_region_tags(sample_text):
    """Remove blank lines and region tags from sample text"""
    magic_lines = [
        line for line in sample_text.split("\n") if len(line) > 0 and "# [" not in line
    ]
    return "\n".join(magic_lines)
