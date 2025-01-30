# Copyright 2021 Google LLC
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

# This is a test configuration file. It is not a part of the sample.

TEST_CONFIG_OVERRIDE = {
    # You can opt out from the test for specific Python versions.
    # > ℹ️ We're opting out of all Python versions except 3.11.
    # > The Python version used is defined by the Dockerfile, so it's redundant
    # > to run multiple tests since they would all be running the same Dockerfile.
    "ignored_versions": ["2.7", "3.6", "3.7", "3.8", "3.9", "3.10", "3.12", "3.13"],
}
