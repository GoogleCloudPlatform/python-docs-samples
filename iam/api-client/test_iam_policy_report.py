# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pytest
import random

import access
import iam_policy_report

# Setting up variables for testing
GCLOUD_PROJECT = os.environ["GCLOUD_PROJECT"]

# specifying a sample role to be assigned
GCP_ROLE = "roles/owner"


@def test_iam_policy_report(capsys):
    iam_policy_report.generatePolicyReport()
 
