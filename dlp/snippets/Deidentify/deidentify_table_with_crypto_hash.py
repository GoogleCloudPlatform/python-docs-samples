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

"""Uses of the Data Loss Prevention API for de-identifying sensitive data
contained in table."""

from __future__ import annotations

import argparse


# [START dlp_deidentify_table_with_crypto_hash]
from typing import Dict, List, Union

import google.cloud.dlp


def deidentify_table_with_crypto_hash(
    project: str,
    table_data: Dict[str, Union[List[str], List[List[str]]]],
    info_types: List[str],
    transient_key_name: str,
) -> None:
    """Uses the Data Loss Prevention API to de-identify sensitive data
    in a table using a cryptographic hash transformation.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        table_data: Dictionary representing table data.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
        transient_key_name: Name of the transient crypto key used for encryption.
            The scope of this key is a single API call. It is generated for
            the transformation and then discarded.
    """

    # Instantiate a client
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct the `table`. For more details on the table schema, please see
    # https://cloud.google.com/dlp/docs/reference/rest/v2/ContentItem#Table
    headers = [{"name": val} for val in table_data["header"]]
    rows = []
    for row in table_data["rows"]:
        rows.append({"values": [{"string_value": cell_val} for cell_val in row]})

    table = {"headers": headers, "rows": rows}

    # Construct the `item` that service will de-identify.
    item = {"table": table}

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries.
    info_types = [{"name": info_type} for info_type in info_types]

    # Construct cryptographic hash configuration using the transient key
    # which will encrypt the data.
    crypto_hash_config = {"crypto_key": {"transient": {"name": transient_key_name}}}

    # Specify the type of info the inspection will look for.
    inspect_config = {
        "info_types": info_types,
    }

    # Construct deidentify configuration dictionary.
    deidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {
                    "info_types": info_types,
                    "primitive_transformation": {
                        "crypto_hash_config": crypto_hash_config
                    },
                }
            ]
        }
    }

    # Convert the project id into a full resource id.
    parent = f"projects/{project}/locations/global"

    # Call the API.
    response = dlp.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": deidentify_config,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    # Print the result.
    print(f"Table after de-identification: {response.item.table}")


# [END dlp_deidentify_table_with_crypto_hash]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "table_data",
        help="Dictionary representing table data",
    )
    parser.add_argument(
        "--info_types",
        action="append",
        help="Strings representing infoTypes to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". ',
    )
    parser.add_argument(
        "transient_key_name",
        help="Name of the transient crypto key used for encryption.",
    )

    args = parser.parse_args()

    deidentify_table_with_crypto_hash(
        args.project,
        args.table_data,
        args.info_types,
        args.transient_key_name,
    )
