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


import os


# We are reaching maximum number of HMAC keys on the service account.
# We change the service account based on the value of
# RUN_TESTS_SESSION. The reason we can not use multiple project is
# that our new projects are enforced to have
# 'constraints/iam.disableServiceAccountKeyCreation' policy.
def get_service_account_email() -> str:
    session = os.environ.get("RUN_TESTS_SESSION")
    if session == "py-3.6":
        return "py36-storage-test@" "python-docs-samples-tests.iam.gserviceaccount.com"
    if session == "py-3.7":
        return "py37-storage-test@" "python-docs-samples-tests.iam.gserviceaccount.com"
    if session == "py-3.8":
        return "py38-storage-test@" "python-docs-samples-tests.iam.gserviceaccount.com"
    return os.environ["HMAC_KEY_TEST_SERVICE_ACCOUNT"]


TEST_CONFIG_OVERRIDE = {
    # A dictionary you want to inject into your test. Don't put any
    # secrets here. These values will override predefined values.
    "envs": {
        "HMAC_KEY_TEST_SERVICE_ACCOUNT": get_service_account_email(),
        # Some tests can not use multiple projects because of several reasons:
        # 1. The new projects is enforced to have the
        # 'constraints/iam.disableServiceAccountKeyCreation' policy.
        # 2. The new projects buckets need to have universal permission model.
        # For those tests, we'll use the original project.
        "MAIN_GOOGLE_CLOUD_PROJECT": "python-docs-samples-tests",
    },
}
