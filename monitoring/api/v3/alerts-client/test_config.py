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

import os

# Temporary set BUILD_SPECIFIC_GCLOUD_PROJECT in this file.
os.environ['BUILD_SPECIFIC_GCLOUD_PROJECT'] = 'tmatsuo-test'

# Default TEST_CONFIG_OVERRIDE for python repos.

# You can copy this file into your directory, then it will be inported from
# the noxfile.py.

# The source of truth:
# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/test_config.py

TEST_CONFIG_OVERRIDE = {
    # You can opt out from the test for specific Python versions.
    'ignored_versions': ["2.7"],

    # Declare optional test sessions you want to opt-in. Currently we
    # have the following optional test sessions:
    #     'cloud_run' # Test session for Cloud Run application.
    'opt_in_sessions': [],

    # Only relevant for the `cloud_run` session. Specify the file
    # names for your e2e test.
    'cloud_run_e2e_test_files': ['e2e_test.py'],

    # If set to True, the test will install the library from the root
    # of the repository.
    'install_library_from_source': False,

    # Set to True if you want to use the Cloud Project configured for each
    # build.
    'use_build_specific_project': True,

    # An envvar key for determining the build specific project. Normally you
    # don't have to modify this.
    'build_specific_project_env': 'BUILD_SPECIFIC_GCLOUD_PROJECT',

    # A dictionary you want to inject into your test. Don't put any
    # secrets here. These values will override predefined values.
    'envs': {},
}
