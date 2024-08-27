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


# [START dlp_update_stored_infotype]
import google.cloud.dlp


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
    stored_info_type_name = (
        f"projects/{project}/locations/global/storedInfoTypes/{stored_info_type_id}"
    )

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
        "gcs_input_file_path",
        help="The url in the format <bucket>/<path_to_file> for the "
        "location of the source term list.",
    )
    parser.add_argument(
        "output_bucket_name",
        help="The name of the bucket in Google Cloud Storage that "
        "would store the created dictionary.",
    )

    args = parser.parse_args()

    update_stored_infotype(
        args.project,
        args.stored_info_type_id,
        args.gcs_input_file_path,
        args.output_bucket_name,
    )
