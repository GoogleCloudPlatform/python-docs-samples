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


def analyze_iam_policy_longrunning_gcs(project_id, dump_file_path):
    # [START asset_quickstart_analyze_iam_policy_longrunning_gcs]
    from google.cloud import asset_v1

    # TODO project_id = 'Your Google Cloud Project ID'
    # TODO dump_file_path = 'Your analysis dump file path'

    client = asset_v1.AssetServiceClient()
    parent = "projects/{}".format(project_id)

    # Build analysis query
    analysis_query = asset_v1.IamPolicyAnalysisQuery()
    analysis_query.scope = parent
    analysis_query.resource_selector.full_resource_name = f"//cloudresourcemanager.googleapis.com/{parent}"
    analysis_query.options.expand_groups = True
    analysis_query.options.output_group_edges = True

    output_config = asset_v1.IamPolicyAnalysisOutputConfig()
    output_config.gcs_destination.uri = dump_file_path
    operation = client.analyze_iam_policy_longrunning(
        request={"analysis_query": analysis_query, "output_config": output_config}
    )

    operation.result(300)
    print(operation.done())
    # [END asset_quickstart_analyze_iam_policy_longrunning_gcs]


def analyze_iam_policy_longrunning_bigquery(project_id, dataset, table):
    # [START asset_quickstart_analyze_iam_policy_longrunning_bigquery]
    from google.cloud import asset_v1

    # TODO project_id = 'Your Google Cloud Project ID'
    # TODO dataset = 'Your BigQuery dataset path'
    # TODO table = 'Your BigQuery table name'

    client = asset_v1.AssetServiceClient()
    parent = "projects/{}".format(project_id)

    # Build analysis query
    analysis_query = asset_v1.IamPolicyAnalysisQuery()
    analysis_query.scope = parent
    analysis_query.resource_selector.full_resource_name = f"//cloudresourcemanager.googleapis.com/{parent}"
    analysis_query.options.expand_groups = True
    analysis_query.options.output_group_edges = True

    output_config = asset_v1.IamPolicyAnalysisOutputConfig()
    output_config.bigquery_destination.dataset = dataset
    output_config.bigquery_destination.table_prefix = table
    output_config.bigquery_destination.write_disposition = "WRITE_TRUNCATE"
    operation = client.analyze_iam_policy_longrunning(
        request={"analysis_query": analysis_query, "output_config": output_config}
    )

    operation.result(300)
    print(operation.done())
    # [END asset_quickstart_analyze_iam_policy_longrunning_bigquery]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="Your Google Cloud project ID")
    parser.add_argument(
        "dump_file_path",
        help="The GCS file that the analysis results will be dumped to, "
        "e.g.: gs://<bucket-name>/analysis_dump_file",
    )
    parser.add_argument(
          "dataset",
          help="The BigQuery dataset that analysis results will be exported to, "
          "e.g.: my_dataset",
      )
    parser.add_argument(
          "table_prefix",
          help="The prefix of the BigQuery table that analysis results will be exported to, "
          "e.g.: my_table",
      )

    args = parser.parse_args()

    analyze_iam_policy_longrunning_gcs(args.project_id, args.dump_file_path)
    analyze_iam_policy_longrunning_bigquery(args.project_id, args.dataset, args.table_prefix)
