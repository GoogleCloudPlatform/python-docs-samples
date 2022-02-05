# Copyright 2022 Google LLC
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

import google.auth
import pytest
from google.cloud import billing


from main import _is_billing_enabled
from main import _disable_billing_for_project


PROJECT_ID = google.auth.default()[1]
cloud_billing_client = billing.CloudBillingClient()

project_path = cloud_billing_client.common_project_path(PROJECT_ID)


def test__is_billing_enabled():
    # Test project will always have billing enabled
    assert _is_billing_enabled(project_path) == True


def test__disable_billing_for_project():
    # Disabling billing on a live CI project might
    # undesirable side effects on project resources.
    # Figure out a way to test this in non-destructive maner
    pytest.fail()
