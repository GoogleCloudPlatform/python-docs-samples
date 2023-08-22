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
import os


# [START dlp_create_stored_infotype]
import google.cloud.dlp  # noqa: F811, E402


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
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.create_stored_info_type(
        request={
            "parent": parent,
            "config": stored_info_type_config,
            "stored_info_type_id": stored_info_type_id,
        }
    )

    # Print the result
    print("Created Stored InfoType: {}".format(response.name))


# [END dlp_create_stored_infotype]


# [START dlp_update_stored_infotype]
import google.cloud.dlp  # noqa: F811, E402


def update_stored_infotype(
    project: str,
    stored_info_type_id: str,
    gcs_input_file_path: str,
    output_bucket_name: str,
) -> None:
    """Uses the Data Loss Prevention API to update stored infoType
    detector by changing the source term list from one stored in Bigquery
    to one stored in Cloud Storage.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        stored_info_type_id: The identifier of stored infoType which is to
            be updated.
        gcs_input_file_path: The url in the format <bucket>/<path_to_file>
            for the location of the source term list.
        output_bucket_name: The name of the bucket in Google Cloud Storage
            where large dictionary is stored.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct the stored infoType configuration dictionary.
    stored_info_type_config = {
        "large_custom_dictionary": {
            "output_path": {"path": f"gs://{output_bucket_name}"},
            "cloud_storage_file_set": {"url": f"gs://{gcs_input_file_path}"},
        }
    }

    # Set mask to control which fields get updated. For more details, refer
    # https://protobuf.dev/reference/protobuf/google.protobuf/#field-mask
    # for constructing the field mask paths.
    field_mask = {"paths": ["large_custom_dictionary.cloud_storage_file_set.url"]}

    # Convert the stored infoType id into a full resource id.
    stored_info_type_name = f"projects/{project}/storedInfoTypes/{stored_info_type_id}"

    # Call the API.
    response = dlp.update_stored_info_type(
        request={
            "name": stored_info_type_name,
            "config": stored_info_type_config,
            "update_mask": field_mask,
        }
    )

    # Print the result
    print(f"Updated stored infoType successfully: {response.name}")


# [END dlp_update_stored_infotype]


# [START dlp_inspect_with_stored_infotype]
import google.cloud.dlp  # noqa: F811, E402


def inspect_with_stored_infotype(
    project: str,
    stored_info_type_id: str,
    content_string: str,
) -> None:

    """Uses the Data Loss Prevention API to inspect/scan content using stored
    infoType.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        content_string: The string to inspect.
        stored_info_type_id: The identifier of stored infoType used to inspect.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert stored infoType id into full resource id
    stored_type_name = f"projects/{project}/storedInfoTypes/{stored_info_type_id}"

    # Construct a custom info type dictionary using stored infoType.
    custom_info_types = [
        {
            "info_type": {"name": "STORED_TYPE"},
            "stored_type": {
                "name": stored_type_name,
            }
        }
    ]

    # Construct the inspection configuration dictionary.
    inspect_config = {
        "custom_info_types": custom_info_types,
        "include_quote": True,
    }

    # Construct the `item` to be inspected using stored infoType.
    item = {"value": content_string}

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.inspect_content(
        request={
            "parent": parent,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    # Print out the results.
    if response.result.findings:
        for finding in response.result.findings:
            print("Quote: {}".format(finding.quote))
            print("Info type: {}".format(finding.info_type.name))
            print("Likelihood: {}".format(finding.likelihood))
    else:
        print("No findings.")

# [END dlp_inspect_with_stored_infotype]


if __name__ == "__main__":
    default_project = os.environ.get("GOOGLE_CLOUD_PROJECT")

    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(
        dest="content", help="Select how to submit content to the API."
    )
    subparsers.required = True

    parser_create = subparsers.add_parser("create", help="Creates a stored infoType.")
    parser_create.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
        default=default_project,
    )
    parser_create.add_argument(
        "stored_info_type_id",
        help="The identifier for large custom dictionary.",
    )
    parser_create.add_argument(
        "output_bucket_name",
        help="The name of the bucket in Google Cloud Storage that "
        "would store the created dictionary.",
    )

    parser_update = subparsers.add_parser("update", help="Updates the stored infoType.")
    parser_update.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
        default=default_project,
    )
    parser_update.add_argument(
        "stored_info_type_id",
        help="The identifier for large custom dictionary.",
    )
    parser_update.add_argument(
        "gcs_input_file_path",
        help="The url in the format <bucket>/<path_to_file> for the "
        "location of the source term list.",
    )
    parser_update.add_argument(
        "output_bucket_name",
        help="The name of the bucket in Google Cloud Storage that "
        "would store the created dictionary.",
    )

    parser_inspect = subparsers.add_parser(
        "inspect",
        help="Inspects data using stored infoType.",
    )
    parser_inspect.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
        default=default_project,
    )
    parser_inspect.add_argument(
        "stored_info_type_id",
        help="The identifier for large custom dictionary.",
    )
    parser_inspect.add_argument(
        "content_string",
        help="The string to inspect.",
    )

    args = parser.parse_args()

    if args.content == "create":
        create_stored_infotype(
            args.project,
            args.stored_info_type_id,
            args.output_bucket_name,
        )
    elif args.content == "update":
        update_stored_infotype(
            args.project,
            args.stored_info_type_id,
            args.gcs_input_file_path,
            args.output_bucket_name,
        )
    elif args.content == "inspect":
        inspect_with_stored_infotype(
            args.project,
            args.stored_info_type_id,
            args.content_string,
        )
