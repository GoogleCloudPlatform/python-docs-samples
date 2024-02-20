# Copyright 2023 Google LLC
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

"""Sample app that queries the Data Loss Prevention API for stored
infoTypes."""


import argparse


# [START dlp_create_stored_infotype]
import google.cloud.dlp


def create_stored_infotype(
    project: str,
    stored_info_type_id: str,
    output_bucket_name: str,
) -> None:
    """Uses the Data Loss Prevention API to create stored infoType.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        stored_info_type_id: The identifier for large custom dictionary.
        output_bucket_name: The name of the bucket in Google Cloud Storage
            that would store the created dictionary.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct the stored infoType Configuration dictionary. This example creates
    # a stored infoType from a term list stored in a publicly available BigQuery
    # database (bigquery-public-data.samples.github_nested).
    # The database contains all GitHub usernames used in commits.
    stored_info_type_config = {
        "display_name": "GitHub usernames",
        "description": "Dictionary of GitHub usernames used in commits",
        "large_custom_dictionary": {
            "output_path": {"path": f"gs://{output_bucket_name}"},
            # We can either use bigquery field or gcs file as a term list input option.
            "big_query_field": {
                "table": {
                    "project_id": "bigquery-public-data",
                    "dataset_id": "samples",
                    "table_id": "github_nested",
                },
                "field": {"name": "actor"},
            },
        },
    }

    # Convert the project id into a full resource id.
    parent = f"projects/{project}/locations/global"

    # Call the API.
    response = dlp.create_stored_info_type(
        request={
            "parent": parent,
            "config": stored_info_type_config,
            "stored_info_type_id": stored_info_type_id,
        }
    )

    # Print the result
    print(f"Created Stored InfoType: {response.name}")


# [END dlp_create_stored_infotype]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "stored_info_type_id",
        help="The identifier for large custom dictionary.",
    )
    parser.add_argument(
        "output_bucket_name",
        help="The name of the bucket in Google Cloud Storage that "
        "would store the created dictionary.",
    )

    args = parser.parse_args()

    create_stored_infotype(
        args.project,
        args.stored_info_type_id,
        args.output_bucket_name,
    )
