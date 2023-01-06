# Copyright 2020 Google LLC
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

# Default TEST_CONFIG_OVERRIDE for python repos.

# You can copy this file into your directory, then it will be imported from
# the noxfile.py.

# The source of truth:
# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/noxfile_config.py

TEST_CONFIG_OVERRIDE = {
    # You can opt out specific Python versions from the test.
    # To save resources, please consider testing 2 versions at most.
    # Test min and max supported versions which are python 3.7 and 3.11
    # Ignoring python 2.7 which is no longer supported.
    "ignored_versions": ["2.7", "3.8", "3.9", "3.10"],

    # An envvar key for determining the project id to use. Change it
    # to 'BUILD_SPECIFIC_GCLOUD_PROJECT' if you want to opt in using a
    # build specific Cloud project. You can also use your own string
    # to use your own Cloud project.
    # 'gcloud_project_env': 'GOOGLE_CLOUD_PROJECT',
    'gcloud_project_env': 'BUILD_SPECIFIC_GCLOUD_PROJECT',

    # A dictionary you want to inject into your test. Don't put any
    # secrets here. These values will override predefined values.
    'envs': {},
}
