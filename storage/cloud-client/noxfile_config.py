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
# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/noxfile_config.py

import os


# We are reaching maximum number of HMAC keys on the service account.
# We change the service account based on the value of
# RUN_TESTS_SESSION. The reason we can not use multiple project is
# that our new projects are enforced to have
# 'constraints/iam.disableServiceAccountKeyCreation' policy.
def get_service_account_email():
    session = os.environ.get('RUN_TESTS_SESSION')
    if session == 'py-3.6':
        return ('py36-storage-test@'
                'python-docs-samples-tests.iam.gserviceaccount.com')
    if session == 'py-3.7':
        return ('py37-storage-test@'
                'python-docs-samples-tests.iam.gserviceaccount.com')
    if session == 'py-3.8':
        return ('py38-storage-test@'
                'python-docs-samples-tests.iam.gserviceaccount.com')
    if session == 'py-3.9':
        return ('py39-storage-test@'
                'python-docs-samples-tests.iam.gserviceaccount.com')
    if session == 'py-3.10':
        return ('py310-storage-test@'
                'python-docs-samples-tests.iam.gserviceaccount.com')
    return os.environ['HMAC_KEY_TEST_SERVICE_ACCOUNT']


# We change the value of CLOUD_KMS_KEY based on the value of
# RUN_TESTS_SESSION.
def get_cloud_kms_key():
    session = os.environ.get('RUN_TESTS_SESSION')
    if session == 'py-3.6':
        return ('projects/python-docs-samples-tests-py36/locations/us/'
                'keyRings/gcs-kms-key-ring/cryptoKeys/gcs-kms-key')
    if session == 'py-3.7':
        return ('projects/python-docs-samples-tests-py37/locations/us/'
                'keyRings/gcs-kms-key-ring/cryptoKeys/gcs-kms-key')
    if session == 'py-3.8':
        return ('projects/python-docs-samples-tests-py38/locations/us/'
                'keyRings/gcs-kms-key-ring/cryptoKeys/gcs-kms-key')
    if session == 'py-3.9':
        return ('projects/python-docs-samples-tests-py39/locations/us/'
                'keyRings/gcs-kms-key-ring/cryptoKeys/gcs-kms-key')
    if session == 'py-3.10':
        return ('projects/python-docs-samples-tests-310/locations/us/'
                'keyRings/gcs-kms-key-ring/cryptoKeys/gcs-kms-key')
    return os.environ['CLOUD_KMS_KEY']


TEST_CONFIG_OVERRIDE = {
    # You can opt out from the test for specific Python versions.
    'ignored_versions': ["2.7"],

    # An envvar key for determining the project id to use. Change it
    # to 'BUILD_SPECIFIC_GCLOUD_PROJECT' if you want to opt in using a
    # build specific Cloud project. You can also use your own string
    # to use your own Cloud project.
    # 'gcloud_project_env': 'GOOGLE_CLOUD_PROJECT',
    'gcloud_project_env': 'BUILD_SPECIFIC_GCLOUD_PROJECT',

    # A dictionary you want to inject into your test. Don't put any
    # secrets here. These values will override predefined values.
    'envs': {
        'HMAC_KEY_TEST_SERVICE_ACCOUNT': get_service_account_email(),
        'CLOUD_KMS_KEY': get_cloud_kms_key(),
        # Some tests can not use multiple projects because of several reasons:
        # 1. The new projects is enforced to have the
        # 'constraints/iam.disableServiceAccountKeyCreation' policy.
        # 2. The new projects buckets need to have universal permission model.
        # For those tests, we'll use the original project.
        'MAIN_GOOGLE_CLOUD_PROJECT': 'python-docs-samples-tests'
    },
}
