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

# [START dlp_deidentify_table_row_suppress]
from typing import Dict, List, Union  # noqa: F811, E402, I100

import google.cloud.dlp  # noqa: F811, E402


def deidentify_table_suppress_row(
    project: str,
    table_data: Dict[str, Union[List[str], List[List[str]]]],
    condition_field: str,
    condition_operator: str,
    condition_value: int,
) -> None:
    """ Uses the Data Loss Prevention API to de-identify sensitive data in a
      table by suppressing entire row/s based on a condition.

    Args:
        project: The Google Cloud project id to use as a parent resource.
        table_data: Dictionary representing table data.
        condition_field: A table field within the record this condition is evaluated against.
        condition_operator: Operator used to compare the field or infoType to the value. One of:
            RELATIONAL_OPERATOR_UNSPECIFIED, EQUAL_TO, NOT_EQUAL_TO, GREATER_THAN, LESS_THAN, GREATER_THAN_OR_EQUALS,
            LESS_THAN_OR_EQUALS, EXISTS.
        condition_value: Value to compare against. [Mandatory, except for ``EXISTS`` tests.].

    Example:

    >> $ python deid.py deid_table_row_suppress \
    '{"header": ["email", "phone number", "age"],
    "rows": [["robertfrost@example.com", "4232342345", "35"],
    ["johndoe@example.com", "4253458383", "64"]]}' \
    "age" "GREATER_THAN" 50
    >> '{"header": ["email", "phone number", "age"],
        "rows": [["robertfrost@example.com", "4232342345", "35", "21"]]}'
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct the `table`. For more details on the table schema, please see
    # https://cloud.google.com/dlp/docs/reference/rest/v2/ContentItem#Table
    headers = [{"name": val} for val in table_data["header"]]
    rows = []
    for row in table_data["rows"]:
        rows.append({"values": [{"string_value": cell_val} for cell_val in row]})

    table = {"headers": headers, "rows": rows}

    # Construct the `item` containing the table data.
    item = {"table": table}

    # Construct condition list.
    condition = [
        {
            "field": {"name": condition_field},
            "operator": condition_operator,
            "value": {"integer_value": condition_value},
        }
    ]

    # Construct deidentify configuration dictionary
    deidentify_config = {
        "record_transformations": {
            "record_suppressions": [
                {
                    "condition": {
                        "expressions": {"conditions": {"conditions": condition}}
                    }
                }
            ]
        }
    }

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.deidentify_content(
        request={"parent": parent, "deidentify_config": deidentify_config, "item": item}
    )

    # Print the result.
    print("Table after de-identification: {}".format(response.item.table))


# [END dlp_deidentify_table_row_suppress]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(
        dest="content", help="Select how to submit content to the API."
    )
    subparsers.required = True

    table_fpe_parser = subparsers.add_parser(
        "deid_table_fpe",
        help="Deidentify sensitive data in a string using Format Preserving "
        "Encryption (FPE).",
    )
    table_fpe_parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    table_fpe_parser.add_argument(
        "table_header",
        help="List of strings representing table field names.",
    )
    table_fpe_parser.add_argument(
        "table_rows",
        help="List of rows representing table data",
    )
    table_fpe_parser.add_argument(
        "deid_field_names",
        help="A list of fields in table to de-identify.",
    )
    table_fpe_parser.add_argument(
        "key_name",
        help="The name of the Cloud KMS key used to encrypt ('wrap') the "
        "AES-256 key. Example: "
        "key_name = 'projects/YOUR_GCLOUD_PROJECT/locations/YOUR_LOCATION/"
        "keyRings/YOUR_KEYRING_NAME/cryptoKeys/YOUR_KEY_NAME'",
    )
    table_fpe_parser.add_argument(
        "wrapped_key",
        help="The encrypted ('wrapped') AES-256 key to use. This key should "
        "be encrypted using the Cloud KMS key specified by key_name.",
    )
    table_fpe_parser.add_argument(
        "-a",
        "--alphabet",
        default="ALPHA_NUMERIC",
        help="The set of characters to replace sensitive ones with. Commonly "
        'used subsets of the alphabet include "NUMERIC", "HEXADECIMAL", '
        '"UPPER_CASE_ALPHA_NUMERIC", "ALPHA_NUMERIC", '
        '"FFX_COMMON_NATIVE_ALPHABET_UNSPECIFIED"',
    )

    reid_table_fpe_parser = subparsers.add_parser(
        "reid_table_fpe",
        help="Re-identify sensitive data in a table using Format Preserving "
        "Encryption (FPE).",
    )
    reid_table_fpe_parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    reid_table_fpe_parser.add_argument(
        "table_header",
        help="List of strings representing table field names.",
    )
    reid_table_fpe_parser.add_argument(
        "table_rows",
        help="List of rows representing table data",
    )
    reid_table_fpe_parser.add_argument(
        "reid_field_names",
        help="A list of fields in table to re-identify.",
    )
    reid_table_fpe_parser.add_argument(
        "key_name",
        help="The name of the Cloud KMS key used to encrypt ('wrap') the "
        "AES-256 key. Example: "
        "key_name = 'projects/YOUR_GCLOUD_PROJECT/locations/YOUR_LOCATION/"
        "keyRings/YOUR_KEYRING_NAME/cryptoKeys/YOUR_KEY_NAME'",
    )
    reid_table_fpe_parser.add_argument(
        "wrapped_key",
        help="The encrypted ('wrapped') AES-256 key to use. This key should "
        "be encrypted using the Cloud KMS key specified by key_name.",
    )
    reid_table_fpe_parser.add_argument(
        "-a",
        "--alphabet",
        default="ALPHA_NUMERIC",
        help="The set of characters to replace sensitive ones with. Commonly "
        'used subsets of the alphabet include "NUMERIC", "HEXADECIMAL", '
        '"UPPER_CASE_ALPHA_NUMERIC", "ALPHA_NUMERIC", '
        '"FFX_COMMON_NATIVE_ALPHABET_UNSPECIFIED"',
    )

    crypto_hash_parser = subparsers.add_parser(
        "deid_table_crypto_hash",
        help="De-identify sensitive data in a table using a cryptographic "
        "hash transformation.",
    )
    crypto_hash_parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    crypto_hash_parser.add_argument(
        "table_data",
        help="Dictionary representing table data",
    )
    crypto_hash_parser.add_argument(
        "--info_types",
        action="append",
        help="Strings representing infoTypes to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". ',
    )
    crypto_hash_parser.add_argument(
        "transient_key_name",
        help="Name of the transient crypto key used for encryption.",
    )

    multiple_crypto_hash_parser = subparsers.add_parser(
        "deid_table_multiple_crypto_hash",
        help="De-identify sensitive data in a table using multiple transient "
        "cryptographic hash keys.",
    )
    multiple_crypto_hash_parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    multiple_crypto_hash_parser.add_argument(
        "table_data",
        help="Dictionary representing table data",
    )
    multiple_crypto_hash_parser.add_argument(
        "--info_types",
        action="append",
        help="Strings representing infoTypes to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". ',
    )
    multiple_crypto_hash_parser.add_argument(
        "transient_key_name_1",
        help="Name of the first transient crypto key used for encryption.",
    )
    multiple_crypto_hash_parser.add_argument(
        "transient_key_name_2",
        help="Name of the second transient crypto key used for encryption.",
    )
    multiple_crypto_hash_parser.add_argument(
        "deid_fields_1",
        help="List of column names in table to de-identify using transient_key_name_1.",
    )
    multiple_crypto_hash_parser.add_argument(
        "deid_fields_2",
        help="List of column names in table to de-identify using transient_key_name_2.",
    )

    table_bucketing_parser = subparsers.add_parser(
        "deid_table_bucketing",
        help="De-identify sensitive data in a table by replacing "
        "them with fixed size bucket ranges.",
    )
    table_bucketing_parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    table_bucketing_parser.add_argument(
        "--table_data",
        help="Json string representing table data",
    )
    table_bucketing_parser.add_argument(
        "--deid_content_list", help="A list of fields in table to de-identify."
    )
    table_bucketing_parser.add_argument(
        "--bucket_size",
        help="Size of each bucket for fixed sized bucketing.",
    )
    table_bucketing_parser.add_argument(
        "--bucketing_lower_bound",
        help="Lower bound value of buckets.",
    )
    table_bucketing_parser.add_argument(
        "--bucketing_upper_bound",
        help="Upper bound value of buckets.",
    )

    table_primitive_bucketing_parser = subparsers.add_parser(
        "deid_table_primitive_bucketing",
        help="De-identify sensitive data in a table by replacing them "
        "with generalized bucket labels.",
    )
    table_primitive_bucketing_parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
    )

    table_condition_replace_parser = subparsers.add_parser(
        "deid_table_condition_replace",
        help="De-identify sensitive data in a table by replacing "
        "them with info-types based on a condition.",
    )
    table_condition_replace_parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    table_condition_replace_parser.add_argument(
        "table_data",
        help="Json string representing table data",
    )
    table_condition_replace_parser.add_argument(
        "deid_content_list", help="A list of fields in table to de-identify."
    )
    table_condition_replace_parser.add_argument(
        "--info_types",
        nargs="+",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". ',
    )
    table_condition_replace_parser.add_argument(
        "--condition_field",
        help="A table Field within the record this condition is evaluated " "against.",
    )
    table_condition_replace_parser.add_argument(
        "--condition_operator",
        help="Operator used to compare the field or infoType to the value. "
        "One of: RELATIONAL_OPERATOR_UNSPECIFIED, EQUAL_TO, NOT_EQUAL_TO, "
        "GREATER_THAN, LESS_THAN, GREATER_THAN_OR_EQUALS, LESS_THAN_OR_EQUALS, "
        "EXISTS.",
    )
    table_condition_replace_parser.add_argument(
        "--condition_value",
        help="Value to compare against. [Mandatory, except for ``EXISTS`` tests.].",
    )

    table_condition_mask_parser = subparsers.add_parser(
        "deid_table_condition_mask",
        help="De-identify sensitive data in a table by masking"
        "them based on a condition.",
    )
    table_condition_mask_parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    table_condition_mask_parser.add_argument(
        "table_data",
        help="Json string representing table data",
    )
    table_condition_mask_parser.add_argument(
        "deid_content_list", help="A list of fields in table to de-identify."
    )
    table_condition_mask_parser.add_argument(
        "--condition_field",
        help="A table Field within the record this condition is evaluated " "against.",
    )
    table_condition_mask_parser.add_argument(
        "--condition_operator",
        help="Operator used to compare the field or infoType to the value. "
        "One of: RELATIONAL_OPERATOR_UNSPECIFIED, EQUAL_TO, NOT_EQUAL_TO, "
        "GREATER_THAN, LESS_THAN, GREATER_THAN_OR_EQUALS, LESS_THAN_OR_EQUALS, "
        "EXISTS.",
    )
    table_condition_mask_parser.add_argument(
        "--condition_value",
        help="Value to compare against. [Mandatory, except for ``EXISTS`` tests.].",
    )
    table_condition_mask_parser.add_argument(
        "-m",
        "--masking_character",
        help="The character to mask matching sensitive data with.",
    )

    table_replace_with_infotype_parser = subparsers.add_parser(
        "table_replace_with_infotype",
        help="De-identify sensitive data in a table by replacing it with the "
        "info type of the data.",
    )
    table_replace_with_infotype_parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    table_replace_with_infotype_parser.add_argument(
        "table_data",
        help="Json string representing a table.",
    )
    table_replace_with_infotype_parser.add_argument(
        "--info_types",
        action="append",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". ',
    )
    table_replace_with_infotype_parser.add_argument(
        "deid_content_list",
        help="A list of fields in table to de-identify.",
    )

    table_row_suppress_parser = subparsers.add_parser(
        "deid_table_row_suppress",
        help="De-identify sensitive data in a table by suppressing "
        "entire row/s based on a condition.",
    )
    table_row_suppress_parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    table_row_suppress_parser.add_argument(
        "table_data",
        help="Json string representing table data",
    )
    table_row_suppress_parser.add_argument(
        "--condition_field",
        help="A table Field within the record this condition is evaluated " "against.",
    )
    table_row_suppress_parser.add_argument(
        "--condition_operator",
        help="Operator used to compare the field or infoType to the value. "
        "One of: RELATIONAL_OPERATOR_UNSPECIFIED, EQUAL_TO, NOT_EQUAL_TO, "
        "GREATER_THAN, LESS_THAN, GREATER_THAN_OR_EQUALS, LESS_THAN_OR_EQUALS, "
        "EXISTS.",
    )
    table_row_suppress_parser.add_argument(
        "--condition_value",
        help="Value to compare against. [Mandatory, except for ``EXISTS`` tests.].",
    )

    args = parser.parse_args()

    if args.content == "deid_table_fpe":
        deidentify_table_with_fpe(
            args.project,
            args.table_header,
            args.table_rows,
            args.deid_field_names,
            wrapped_key=base64.b64decode(args.wrapped_key),
            key_name=args.key_name,
            alphabet=args.alphabet,
        )
    elif args.content == "reid_table_fpe":
        reidentify_table_with_fpe(
            args.project,
            args.table_header,
            args.table_rows,
            args.reid_field_names,
            wrapped_key=base64.b64decode(args.wrapped_key),
            key_name=args.key_name,
            alphabet=args.alphabet,
        )
    elif args.content == "deid_table_crypto_hash":
        deidentify_table_with_crypto_hash(
            args.project,
            args.table_data,
            args.info_types,
            args.transient_key_name,
        )
    elif args.content == "deid_table_multiple_crypto_hash":
        deidentify_table_with_multiple_crypto_hash(
            args.project,
            args.table_data,
            args.info_types,
            args.transient_key_name_1,
            args.transient_key_name_2,
            args.deid_fields_1,
            args.deid_fields_2,
        )
    elif args.content == "deid_table_bucketing":
        deidentify_table_bucketing(
            args.project,
            args.table_data,
            args.deid_content_list,
            args.bucket_size,
            args.bucketing_lower_bound,
            args.bucketing_upper_bound,
        )
    elif args.content == "deid_table_primitive_bucketing":
        deidentify_table_primitive_bucketing(
            args.project,
        )
    elif args.content == "deid_table_condition_replace":
        deidentify_table_condition_replace_with_info_types(
            args.project,
            args.table_data,
            args.deid_content_list,
            args.info_types,
            condition_field=args.condition_field,
            condition_operator=args.condition_operator,
            condition_value=args.condition_value,
        )
    elif args.content == "deid_table_condition_mask":
        deidentify_table_condition_masking(
            args.project,
            args.table_data,
            args.deid_content_list,
            condition_field=args.condition_field,
            condition_operator=args.condition_operator,
            condition_value=args.condition_value,
            masking_character=args.masking_character,
        )
    elif args.content == "table_replace_with_infotype":
        deidentify_table_replace_with_info_types(
            args.project,
            args.table_data,
            args.info_types,
            args.deid_content_list,
        )
    elif args.content == "deid_table_row_suppress":
        deidentify_table_suppress_row(
            args.project,
            args.table_data,
            condition_field=args.condition_field,
            condition_operator=args.condition_operator,
            condition_value=args.condition_value,
        )
