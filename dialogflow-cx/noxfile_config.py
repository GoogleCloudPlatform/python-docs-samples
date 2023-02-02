# Copyright 2023 Google LLC
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

# Default TEST_CONFIG_OVERRIDE for python repos.

# You can copy this file into your directory, then it will be inported from
# the noxfile.py.

# The source of truth:
# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/noxfile_config.py

TEST_CONFIG_OVERRIDE = {
    # You can opt out from the test for specific Python versions.
    "ignored_versions": ["2.7"],
    # An envvar key for determining the project id to use. Change it
    # to 'BUILD_SPECIFIC_GCLOUD_PROJECT' if you want to opt in using a
    # build specific Cloud project. You can also use your own string
    # to use your own Cloud project.
    # 'gcloud_project_env': 'BUILD_SPECIFIC_GCLOUD_PROJECT',
    "gcloud_project_env": "GOOGLE_CLOUD_PROJECT",
    # A dictionary you want to inject into your test. Don't put any
    # secrets here. These values will override predefined values.
    "envs": {
        "AGENT_ID": "53516802-3e2a-4016-80b6-a3df0d240240",
        "AGENT_ID_US_CENTRAL1": "edf8372c-c66a-4984-83ba-b85885e95e2a",
        "AUDIO_PATH": "resources/hello.wav",
        "INTENT_ID": "164428bd-647a-4e30-ab0f-cc7f3e3b76f9",
    },
}
