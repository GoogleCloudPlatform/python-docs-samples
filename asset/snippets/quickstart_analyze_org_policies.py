#!/usr/bin/env python

# Copyright 2023 Google LLC.
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


import argparse


def analyze_org_policies(organization_id, constraint):
    # [START asset_quickstart_analyze_org_policies]
    from google.cloud import asset_v1

    # TODO organization_id = 'Your Google Cloud Organization ID'
    # TODO constraint = 'Constraint you want to analyze'
    client = asset_v1.AssetServiceClient()
    scope = f"organizations/{organization_id}"

    response = client.analyze_org_policies(
        request={"scope": scope, "constraint": constraint}
    )
    print(f"Analysis completed successfully: {response}")

    # [END asset_quickstart_analyze_org_policies]
    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("organization_id", help="Your Google Cloud Organization ID")
    parser.add_argument("constraint", help="Constraint you want to analyze")
    args = parser.parse_args()
    analyze_org_policies(args.organization_id, args.constraint)
