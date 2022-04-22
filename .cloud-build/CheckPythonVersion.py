#!/usr/bin/env python
# # Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys

MINIMUM_MAJOR_VERSION = 3
MINIMUM_MINOR_VERSION = 5

if (
    sys.version_info.major >= MINIMUM_MAJOR_VERSION
    or sys.version_info.minor >= MINIMUM_MINOR_VERSION
):
    print(f"Python version acceptable: {sys.version}")
    exit(0)
else:
    print(
        f"Error: Python version less than {MINIMUM_MAJOR_VERSION}.{MINIMUM_MINOR_VERSION}"
    )
    exit(1)
