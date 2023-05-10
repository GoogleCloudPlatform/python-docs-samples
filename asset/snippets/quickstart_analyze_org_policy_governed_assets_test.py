#!/usr/bin/env python

# Copyright 2023 Google LLC. All Rights Reserved.
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

import quickstart_analyze_org_policy_governed_assets

# Owner of the organization below: cloud-asset-analysis-team.
ORG_ID = "474566717491"

# Find more Organization Policy Constraints at:
# http://cloud/resource-manager/docs/organization-policy/org-policy-constraints
CONSTRAINT_NAME = "constraints/compute.requireOsLogin"


def test_analyze_org_policy_governed_assets(capsys):
    quickstart_analyze_org_policy_governed_assets.analyze_org_policy_governed_assets(ORG_ID, CONSTRAINT_NAME)
    out, _ = capsys.readouterr()
    assert CONSTRAINT_NAME in out
