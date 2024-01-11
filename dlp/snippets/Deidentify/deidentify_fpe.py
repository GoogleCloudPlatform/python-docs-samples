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

"""Uses of the Data Loss Prevention API for deidentifying sensitive data."""

from __future__ import annotations

import argparse


# [START dlp_deidentify_fpe]
import base64
from typing import List

import google.cloud.dlp


def deidentify_with_fpe(
    project: str,
    input_str: str,
    info_types: List[str],
    alphabet: str = None,
    surrogate_type: str = None,
    key_name: str = None,
    wrapped_key: str = None,
) -> None:
    """Uses the Data Loss Prevention API to deidentify sensitive data in a
    string using Format Preserving Encryption (FPE).
    Args:
        project: The Google Cloud project id to use as a parent resource.
        input_str: The string to deidentify (will be treated as text).
        info_types: A list of strings representing info types to look for.
        alphabet: The set of characters to replace sensitive ones with. For
            more information, see https://cloud.google.com/dlp/docs/reference/
            rest/v2beta2/organizations.deidentifyTemplates#ffxcommonnativealphabet
        surrogate_type: The name of the surrogate custom info type to use. Only
            necessary if you want to reverse the deidentification process. Can
            be essentially any arbitrary string, as long as it doesn't appear
            in your dataset otherwise.
        key_name: The name of the Cloud KMS key used to encrypt ('wrap') the
            AES-256 key. Example:
            key_name = 'projects/YOUR_GCLOUD_PROJECT/locations/YOUR_LOCATION/
            keyRings/YOUR_KEYRING_NAME/cryptoKeys/YOUR_KEY_NAME'
        wrapped_key: The encrypted ('wrapped') AES-256 key to use. This key
            should be encrypted using the Cloud KMS key specified by key_name.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}/locations/global"

    # The wrapped key is base64-encoded, but the library expects a binary
    # string, so decode it here.
    wrapped_key = base64.b64decode(wrapped_key)

    # Construct FPE configuration dictionary
    crypto_replace_ffx_fpe_config = {
        "crypto_key": {
            "kms_wrapped": {"wrapped_key": wrapped_key, "crypto_key_name": key_name}
        },
        "common_alphabet": alphabet,
    }

    # Add surrogate type
    if surrogate_type:
        crypto_replace_ffx_fpe_config["surrogate_info_type"] = {"name": surrogate_type}

    # Construct inspect configuration dictionary
    inspect_config = {"info_types": [{"name": info_type} for info_type in info_types]}

    # Construct deidentify configuration dictionary
    deidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {
                    "primitive_transformation": {
                        "crypto_replace_ffx_fpe_config": crypto_replace_ffx_fpe_config
                    }
                }
            ]
        }
    }

    # Convert string to item
    item = {"value": input_str}

    # Call the API
    response = dlp.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": deidentify_config,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    # Print results
    print(response.item.value)


# [END dlp_deidentify_fpe]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--info_types",
        action="append",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
        "If unspecified, the three above examples will be used.",
        default=["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"],
    )
    parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "item",
        help="The string to deidentify. " "Example: string = 'My SSN is 372819127'",
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
    parser.add_argument(
        "-s",
        "--surrogate_type",
        help="The name of the surrogate custom info type to use. Only "
        "necessary if you want to reverse the de-identification process. Can "
        "be essentially any arbitrary string, as long as it doesn't appear "
        "in your dataset otherwise.",
    )

    args = parser.parse_args()

    deidentify_with_fpe(
        args.project,
        args.item,
        args.info_types,
        alphabet=args.alphabet,
        wrapped_key=args.wrapped_key,
        key_name=args.key_name,
        surrogate_type=args.surrogate_type,
    )
