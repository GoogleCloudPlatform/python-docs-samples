#!/usr/bin/env python

# Copyright 2020 Google LLC. All Rights Reserved.
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


def analyze_iam_policy(project_id):
    # [START asset_quickstart_analyze_iam_policy]
    from google.cloud import asset_v1

    # TODO project_id = 'Your Google Cloud Project ID'

    client = asset_v1.AssetServiceClient()
    parent = "projects/{}".format(project_id)

    # Build analysis query
    analysis_query = asset_v1.IamPolicyAnalysisQuery()
    analysis_query.scope = parent
    analysis_query.resource_selector.full_resource_name = f"//cloudresourcemanager.googleapis.com/{parent}"
    analysis_query.options.expand_groups = True
    analysis_query.options.output_group_edges = True

    response = client.analyze_iam_policy(
        request={"analysis_query": analysis_query}
    )
    print(response)
    # [END asset_quickstart_analyze_iam_policy]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="Your Google Cloud project ID")

    args = parser.parse_args()

    analyze_iam_policy(args.project_id)
