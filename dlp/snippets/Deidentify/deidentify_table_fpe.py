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
import base64


# [START dlp_deidentify_table_fpe]
from typing import List

import google.cloud.dlp


def deidentify_table_with_fpe(
    project: str,
    table_header: List[str],
    table_rows: List[List[str]],
    deid_field_names: List[str],
    key_name: str = None,
    wrapped_key: bytes = None,
    alphabet: str = None,
) -> None:
    """Uses the Data Loss Prevention API to de-identify sensitive data in a
      table while maintaining format.

    Args:
        project: The Google Cloud project id to use as a parent resource.
        table_header: List of strings representing table field names.
        table_rows: List of rows representing table data.
        deid_field_names: A list of fields in table to de-identify.
        key_name: The name of the Cloud KMS key used to encrypt ('wrap') the
            AES-256 key. Example:
            key_name = 'projects/YOUR_GCLOUD_PROJECT/locations/YOUR_LOCATION/
            keyRings/YOUR_KEYRING_NAME/cryptoKeys/YOUR_KEY_NAME'
        wrapped_key: The decrypted ('wrapped', in bytes) AES-256 key to use. This key
            should be encrypted using the Cloud KMS key specified by key_name.
        alphabet: The set of characters to replace sensitive ones with. For
            more information, see https://cloud.google.com/dlp/docs/reference/
            rest/v2/projects.deidentifyTemplates#ffxcommonnativealphabet
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct the `table`. For more details on the table schema, please see
    # https://cloud.google.com/dlp/docs/reference/rest/v2/ContentItem#Table
    headers = [{"name": val} for val in table_header]
    rows = []
    for row in table_rows:
        rows.append({"values": [{"string_value": cell_val} for cell_val in row]})

    table = {"headers": headers, "rows": rows}

    # Construct the `item` for table.
    item = {"table": table}

    # Specify fields to be de-identified.
    deid_field_names = [{"name": _i} for _i in deid_field_names]

    # Construct FPE configuration dictionary
    crypto_replace_ffx_fpe_config = {
        "crypto_key": {
            "kms_wrapped": {"wrapped_key": wrapped_key, "crypto_key_name": key_name},
        },
        "common_alphabet": alphabet,
    }

    # Construct deidentify configuration dictionary
    deidentify_config = {
        "record_transformations": {
            "field_transformations": [
                {
                    "primitive_transformation": {
                        "crypto_replace_ffx_fpe_config": crypto_replace_ffx_fpe_config
                    },
                    "fields": deid_field_names,
                }
            ]
        }
    }

    # Convert the project id into a full resource id.
    parent = f"projects/{project}/locations/global"

    # Call the API.
    response = dlp.deidentify_content(
        request={"parent": parent, "deidentify_config": deidentify_config, "item": item}
    )

    # Print out results.
    print(f"Table after de-identification: {response.item.table}")


# [END dlp_deidentify_table_fpe]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "table_header",
        help="List of strings representing table field names.",
    )
    parser.add_argument(
        "table_rows",
        help="List of rows representing table data",
    )
    parser.add_argument(
        "deid_field_names",
        help="A list of fields in table to de-identify.",
    )
    parser.add_argument(
        "key_name",
        help="The name of the Cloud KMS key used to encrypt ('wrap') the "
        "AES-256 key. Example: "
        "key_name = 'projects/YOUR_GCLOUD_PROJECT/locations/YOUR_LOCATION/"
        "keyRings/YOUR_KEYRING_NAME/cryptoKeys/YOUR_KEY_NAME'",
    )
    parser.add_argument(
        "wrapped_key",
        help="The encrypted ('wrapped') AES-256 key to use. This key should "
        "be encrypted using the Cloud KMS key specified by key_name.",
    )
    parser.add_argument(
        "-a",
        "--alphabet",
        default="ALPHA_NUMERIC",
        help="The set of characters to replace sensitive ones with. Commonly "
        'used subsets of the alphabet include "NUMERIC", "HEXADECIMAL", '
        '"UPPER_CASE_ALPHA_NUMERIC", "ALPHA_NUMERIC", '
        '"FFX_COMMON_NATIVE_ALPHABET_UNSPECIFIED"',
    )

    args = parser.parse_args()

    deidentify_table_with_fpe(
        args.project,
        args.table_header,
        args.table_rows,
        args.deid_field_names,
        wrapped_key=base64.b64decode(args.wrapped_key),
        key_name=args.key_name,
        alphabet=args.alphabet,
    )
