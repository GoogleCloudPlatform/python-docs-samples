#!/usr/bin/env python

# Copyright 2022 Google LLC.
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


def create_saved_query(project_id, saved_query_id, description):
    # [START asset_quickstart_create_saved_query]
    from google.cloud import asset_v1

    # TODO project_id = 'Your Google Cloud Project ID'
    # TODO saved_query_id = 'SavedQuery ID you want to create'
    client = asset_v1.AssetServiceClient()
    parent = f"projects/{project_id}"
    saved_query = asset_v1.SavedQuery()
    saved_query.description = description

    # TODO: customize your saved query based on the guide below.
    # https://cloud.google.com/asset-inventory/docs/reference/rest/v1/savedQueries#IamPolicyAnalysisQuery
    saved_query.content.iam_policy_analysis_query.scope = parent
    query_access_selector = saved_query.content.iam_policy_analysis_query.access_selector
    query_access_selector.permissions.append("iam.serviceAccounts.actAs")

    response = client.create_saved_query(
        request={
            "parent": parent,
            "saved_query_id": saved_query_id,
            "saved_query": saved_query,
        }
    )
    print(f"saved_query: {response}")
    # [END asset_quickstart_create_saved_query]
    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="Your Google Cloud project ID")
    parser.add_argument("saved_query_id", help="SavedQuery ID you want to create")
    parser.add_argument("description", help="The description of the saved_query")
    args = parser.parse_args()
    create_saved_query(args.project_id, args.saved_query_id, args.description)
