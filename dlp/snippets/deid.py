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


# [START dlp_deidentify_masking]
from typing import List  # noqa: F811, E402

import google.cloud.dlp  # noqa: F811, E402


def deidentify_with_mask(
    project: str,
    input_str: str,
    info_types: List[str],
    masking_character: str = None,
    number_to_mask: int = 0,
) -> None:
    """Uses the Data Loss Prevention API to deidentify sensitive data in a
    string by masking it with a character.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        input_str: The string to deidentify (will be treated as text).
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
        masking_character: The character to mask matching sensitive data with.
        number_to_mask: The maximum number of sensitive characters to mask in
            a match. If omitted or set to zero, the API will default to no
            maximum.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Construct inspect configuration dictionary
    inspect_config = {"info_types": [{"name": info_type} for info_type in info_types]}

    # Construct deidentify configuration dictionary
    deidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {
                    "primitive_transformation": {
                        "character_mask_config": {
                            "masking_character": masking_character,
                            "number_to_mask": number_to_mask,
                        }
                    }
                }
            ]
        }
    }

    # Construct item
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

    # Print out the results.
    print(response.item.value)


# [END dlp_deidentify_masking]


# [START dlp_deidentify_redact]
from typing import List  # noqa: F811, E402, I100

import google.cloud.dlp  # noqa: F811, E402


def deidentify_with_redact(
    project: str,
    input_str: str,
    info_types: List[str],
) -> None:
    """Uses the Data Loss Prevention API to deidentify sensitive data in a
    string by redacting matched input values.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        input_str: The string to deidentify (will be treated as text).
        info_types: A list of strings representing info types to look for.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Construct inspect configuration dictionary
    inspect_config = {"info_types": [{"name": info_type} for info_type in info_types]}

    # Construct deidentify configuration dictionary
    deidentify_config = {
        "info_type_transformations": {
            "transformations": [{"primitive_transformation": {"redact_config": {}}}]
        }
    }

    # Construct item
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

    # Print out the results.
    print(response.item.value)


# [END dlp_deidentify_redact]


# [START dlp_deidentify_replace]
from typing import List  # noqa: F811, E402, I100

import google.cloud.dlp  # noqa: F811, E402


def deidentify_with_replace(
    project: str,
    input_str: str,
    info_types: List[str],
    replacement_str: str = "REPLACEMENT_STR",
) -> None:
    """Uses the Data Loss Prevention API to deidentify sensitive data in a
    string by replacing matched input values with a value you specify.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        input_str: The string to deidentify (will be treated as text).
        info_types: A list of strings representing info types to look for.
        replacement_str: The string to replace all values that match given
            info types.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Construct inspect configuration dictionary
    inspect_config = {"info_types": [{"name": info_type} for info_type in info_types]}

    # Construct deidentify configuration dictionary
    deidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {
                    "primitive_transformation": {
                        "replace_config": {
                            "new_value": {"string_value": replacement_str}
                        }
                    }
                }
            ]
        }
    }

    # Construct item
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

    # Print out the results.
    print(response.item.value)


# [END dlp_deidentify_replace]

# [START dlp_deidentify_fpe]
import base64  # noqa: F811, E402, I100
from typing import List  # noqa: F811, E402

import google.cloud.dlp  # noqa: F811, E402


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
    parent = f"projects/{project}"

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


# [START dlp_reidentify_text_fpe]
import base64  # noqa: F811, E402, I100

import google.cloud.dlp  # noqa: F811, E402


def reidentify_text_with_fpe(
    project: str,
    input_str: str,
    key_name: str = None,
    wrapped_key: str = None,
) -> None:
    """
    Uses the Data Loss Prevention API to re-identify sensitive data in a
    string using Format Preserving Encryption (FPE).
    Args:
        project: The Google Cloud project id to use as a parent resource.
        input_str: The string to re-identify (will be treated as text).
        key_name: The name of the Cloud KMS key used to encrypt ('wrap') the
            AES-256 key. Example:
            key_name = 'projects/YOUR_GCLOUD_PROJECT/locations/YOUR_LOCATION/
            keyRings/YOUR_KEYRING_NAME/cryptoKeys/YOUR_KEY_NAME'
        wrapped_key: The encrypted ('wrapped') AES-256 key to use. This key
            should be encrypted using the Cloud KMS key specified by key_name.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # The wrapped key is base64-encoded, but the library expects a binary
    # string, so decode it here.
    wrapped_key = base64.b64decode(wrapped_key)

    # Specify the type of info the inspection will re-identify.
    # This must use the same custom infoType that was used as a
    # surrogate during the initial encryption.
    surrogate_info_type = {"name": "PHONE_NUMBER"}

    # Construct FPE configuration dictionary
    crypto_replace_ffx_fpe_config = {
        "crypto_key": {
            "kms_wrapped": {"wrapped_key": wrapped_key, "crypto_key_name": key_name}
        },
        "common_alphabet": 'NUMERIC',
        "surrogate_info_type": surrogate_info_type,
    }

    # Construct re-identify configuration dictionary
    reidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {
                    "primitive_transformation": {
                        "crypto_replace_ffx_fpe_config": crypto_replace_ffx_fpe_config,
                    },
                    "info_types": [surrogate_info_type],
                }
            ]
        }
    }

    # Construct inspect configuration dictionary
    inspect_config = {
        "custom_info_types": [
            {"info_type": surrogate_info_type, "surrogate_type": {}}
        ]
    }

    # Construct the `item`.
    item = {"value": input_str}

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.reidentify_content(
        request={
            "parent": parent,
            "reidentify_config": reidentify_config,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    # Print results
    print(f"Text after re-identification: {response.item.value}")


# [END dlp_reidentify_text_fpe]


# [START dlp_deidentify_deterministic]
import base64  # noqa: F811, E402, I100
from typing import List  # noqa: F811, E402

import google.cloud.dlp  # noqa: F811, E402


def deidentify_with_deterministic(
    project: str,
    input_str: str,
    info_types: List[str],
    surrogate_type: str = None,
    key_name: str = None,
    wrapped_key: str = None,
) -> None:
    """Deidentifies sensitive data in a string using deterministic encryption.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        input_str: The string to deidentify (will be treated as text).
        info_types: A list of strings representing info types to look for.
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
    parent = f"projects/{project}"

    # The wrapped key is base64-encoded, but the library expects a binary
    # string, so decode it here.
    wrapped_key = base64.b64decode(wrapped_key)

    # Construct Deterministic encryption configuration dictionary
    crypto_replace_deterministic_config = {
        "crypto_key": {
            "kms_wrapped": {"wrapped_key": wrapped_key, "crypto_key_name": key_name}
        },
    }

    # Add surrogate type
    if surrogate_type:
        crypto_replace_deterministic_config["surrogate_info_type"] = {
            "name": surrogate_type
        }

    # Construct inspect configuration dictionary
    inspect_config = {"info_types": [{"name": info_type} for info_type in info_types]}

    # Construct deidentify configuration dictionary
    deidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {
                    "primitive_transformation": {
                        "crypto_deterministic_config": crypto_replace_deterministic_config
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


# [END dlp_deidentify_deterministic]


# [START dlp_reidentify_fpe]
import base64  # noqa: F811, E402, I100

import google.cloud.dlp  # noqa: F811, E402


def reidentify_with_fpe(
    project: str,
    input_str: str,
    alphabet: str = None,
    surrogate_type: str = None,
    key_name: str = None,
    wrapped_key: str = None,
) -> None:
    """Uses the Data Loss Prevention API to reidentify sensitive data in a
    string that was encrypted by Format Preserving Encryption (FPE).
    Args:
        project: The Google Cloud project id to use as a parent resource.
        input_str: The string to deidentify (will be treated as text).
        alphabet: The set of characters to replace sensitive ones with. For
            more information, see https://cloud.google.com/dlp/docs/reference/
            rest/v2beta2/organizations.deidentifyTemplates#ffxcommonnativealphabet
        surrogate_type: The name of the surrogate custom info type to used
            during the encryption process.
        key_name: The name of the Cloud KMS key used to encrypt ('wrap') the
            AES-256 key. Example:
            keyName = 'projects/YOUR_GCLOUD_PROJECT/locations/YOUR_LOCATION/
            keyRings/YOUR_KEYRING_NAME/cryptoKeys/YOUR_KEY_NAME'
        wrapped_key: The encrypted ('wrapped') AES-256 key to use. This key
            should be encrypted using the Cloud KMS key specified by key_name.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # The wrapped key is base64-encoded, but the library expects a binary
    # string, so decode it here.
    wrapped_key = base64.b64decode(wrapped_key)

    # Construct Deidentify Config
    reidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {
                    "primitive_transformation": {
                        "crypto_replace_ffx_fpe_config": {
                            "crypto_key": {
                                "kms_wrapped": {
                                    "wrapped_key": wrapped_key,
                                    "crypto_key_name": key_name,
                                }
                            },
                            "common_alphabet": alphabet,
                            "surrogate_info_type": {"name": surrogate_type},
                        }
                    }
                }
            ]
        }
    }

    inspect_config = {
        "custom_info_types": [
            {"info_type": {"name": surrogate_type}, "surrogate_type": {}}
        ]
    }

    # Convert string to item
    item = {"value": input_str}

    # Call the API
    response = dlp.reidentify_content(
        request={
            "parent": parent,
            "reidentify_config": reidentify_config,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    # Print results
    print(response.item.value)


# [END dlp_reidentify_fpe]


# [START dlp_reidentify_deterministic]
import base64  # noqa: F811, E402, I100

import google.cloud.dlp  # noqa: F811, E402


def reidentify_with_deterministic(
    project: str,
    input_str: str,
    surrogate_type: str = None,
    key_name: str = None,
    wrapped_key: str = None,
) -> None:
    """Re-identifies content that was previously de-identified through deterministic encryption.
    Args:
        project: The Google Cloud project ID to use as a parent resource.
        input_str: The string to be re-identified. Provide the entire token. Example:
            EMAIL_ADDRESS_TOKEN(52):AVAx2eIEnIQP5jbNEr2j9wLOAd5m4kpSBR/0jjjGdAOmryzZbE/q
        surrogate_type: The name of the surrogate custom infoType used
            during the encryption process.
        key_name: The name of the Cloud KMS key used to encrypt ("wrap") the
            AES-256 key. Example:
            keyName = 'projects/YOUR_GCLOUD_PROJECT/locations/YOUR_LOCATION/
            keyRings/YOUR_KEYRING_NAME/cryptoKeys/YOUR_KEY_NAME'
        wrapped_key: The encrypted ("wrapped") AES-256 key previously used to encrypt the content.
            This key must have been encrypted using the Cloud KMS key specified by key_name.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # The wrapped key is base64-encoded, but the library expects a binary
    # string, so decode it here.
    wrapped_key = base64.b64decode(wrapped_key)

    # Construct reidentify Configuration
    reidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {
                    "primitive_transformation": {
                        "crypto_deterministic_config": {
                            "crypto_key": {
                                "kms_wrapped": {
                                    "wrapped_key": wrapped_key,
                                    "crypto_key_name": key_name,
                                }
                            },
                            "surrogate_info_type": {"name": surrogate_type},
                        }
                    }
                }
            ]
        }
    }

    inspect_config = {
        "custom_info_types": [
            {"info_type": {"name": surrogate_type}, "surrogate_type": {}}
        ]
    }

    # Convert string to item
    item = {"value": input_str}

    # Call the API
    response = dlp.reidentify_content(
        request={
            "parent": parent,
            "reidentify_config": reidentify_config,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    # Print results
    print(response.item.value)


# [END dlp_reidentify_deterministic]


# [START dlp_deidentify_free_text_with_fpe_using_surrogate]
import base64  # noqa: F811, E402, I100

import google.cloud.dlp  # noqa: F811, E402


def deidentify_free_text_with_fpe_using_surrogate(
    project: str,
    input_str: str,
    alphabet: str = "NUMERIC",
    info_type: str = "PHONE_NUMBER",
    surrogate_type: str = "PHONE_TOKEN",
    unwrapped_key: str = "YWJjZGVmZ2hpamtsbW5vcA==",
) -> None:
    """Uses the Data Loss Prevention API to deidentify sensitive data in a
       string using Format Preserving Encryption (FPE).
       The encryption is performed with an unwrapped key.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        input_str: The string to deidentify (will be treated as text).
        alphabet: The set of characters to replace sensitive ones with. For
            more information, see https://cloud.google.com/dlp/docs/reference/
            rest/v2beta2/organizations.deidentifyTemplates#ffxcommonnativealphabet
        info_type: The name of the info type to de-identify
        surrogate_type: The name of the surrogate custom info type to use. Can
            be essentially any arbitrary string, as long as it doesn't appear
            in your dataset otherwise.
        unwrapped_key: The base64-encoded AES-256 key to use.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # The wrapped key is base64-encoded, but the library expects a binary
    # string, so decode it here.
    unwrapped_key = base64.b64decode(unwrapped_key)

    # Construct de-identify config
    transformation = {
        "info_types": [{"name": info_type}],
        "primitive_transformation": {
            "crypto_replace_ffx_fpe_config": {
                "crypto_key": {"unwrapped": {"key": unwrapped_key}},
                "common_alphabet": alphabet,
                "surrogate_info_type": {"name": surrogate_type},
            }
        },
    }

    deidentify_config = {
        "info_type_transformations": {"transformations": [transformation]}
    }

    # Construct the inspect config, trying to finding all PII with likelihood
    # higher than UNLIKELY
    inspect_config = {
        "info_types": [{"name": info_type}],
        "min_likelihood": google.cloud.dlp_v2.Likelihood.UNLIKELY,
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


# [END dlp_deidentify_free_text_with_fpe_using_surrogate]


# [START dlp_reidentify_free_text_with_fpe_using_surrogate]
import base64  # noqa: F811, E402, I100

import google.cloud.dlp  # noqa: F811, E402


def reidentify_free_text_with_fpe_using_surrogate(
    project: str,
    input_str: str,
    alphabet: str = "NUMERIC",
    surrogate_type: str = "PHONE_TOKEN",
    unwrapped_key: str = "YWJjZGVmZ2hpamtsbW5vcA==",
) -> None:
    """Uses the Data Loss Prevention API to reidentify sensitive data in a
    string that was encrypted by Format Preserving Encryption (FPE) with
    surrogate type. The encryption is performed with an unwrapped key.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        input_str: The string to deidentify (will be treated as text).
        alphabet: The set of characters to replace sensitive ones with. For
            more information, see https://cloud.google.com/dlp/docs/reference/
            rest/v2beta2/organizations.deidentifyTemplates#ffxcommonnativealphabet
        surrogate_type: The name of the surrogate custom info type to used
            during the encryption process.
        unwrapped_key: The base64-encoded AES-256 key to use.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # The wrapped key is base64-encoded, but the library expects a binary
    # string, so decode it here.
    unwrapped_key = base64.b64decode(unwrapped_key)

    # Construct Deidentify Config
    transformation = {
        "primitive_transformation": {
            "crypto_replace_ffx_fpe_config": {
                "crypto_key": {"unwrapped": {"key": unwrapped_key}},
                "common_alphabet": alphabet,
                "surrogate_info_type": {"name": surrogate_type},
            }
        }
    }

    reidentify_config = {
        "info_type_transformations": {"transformations": [transformation]}
    }

    inspect_config = {
        "custom_info_types": [
            {"info_type": {"name": surrogate_type}, "surrogate_type": {}}
        ]
    }

    # Convert string to item
    item = {"value": input_str}

    # Call the API
    response = dlp.reidentify_content(
        request={
            "parent": parent,
            "reidentify_config": reidentify_config,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    # Print results
    print(response.item.value)


# [END dlp_reidentify_free_text_with_fpe_using_surrogate]


# [START dlp_deidentify_date_shift]
import base64  # noqa: F811, E402, I100
import csv  # noqa: F811, E402, I100
from datetime import datetime  # noqa: F811, E402, I100
from typing import List  # noqa: F811, E402

import google.cloud.dlp  # noqa: F811, E402
from google.cloud.dlp_v2 import types  # noqa: F811, E402


def deidentify_with_date_shift(
    project: str,
    input_csv_file: str = None,
    output_csv_file: str = None,
    date_fields: List[str] = None,
    lower_bound_days: int = None,
    upper_bound_days: int = None,
    context_field_id: str = None,
    wrapped_key: str = None,
    key_name: str = None,
) -> None:
    """Uses the Data Loss Prevention API to deidentify dates in a CSV file by
        pseudorandomly shifting them.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        input_csv_file: The path to the CSV file to deidentify. The first row
            of the file must specify column names, and all other rows must
            contain valid values.
        output_csv_file: The path to save the date-shifted CSV file.
        date_fields: The list of (date) fields in the CSV file to date shift.
            Example: ['birth_date', 'register_date']
        lower_bound_days: The maximum number of days to shift a date backward
        upper_bound_days: The maximum number of days to shift a date forward
        context_field_id: (Optional) The column to determine date shift amount
            based on. If this is not specified, a random shift amount will be
            used for every row. If this is specified, then 'wrappedKey' and
            'keyName' must also be set. Example:
            contextFieldId = [{ 'name': 'user_id' }]
        key_name: (Optional) The name of the Cloud KMS key used to encrypt
            ('wrap') the AES-256 key. Example:
            key_name = 'projects/YOUR_GCLOUD_PROJECT/locations/YOUR_LOCATION/
            keyRings/YOUR_KEYRING_NAME/cryptoKeys/YOUR_KEY_NAME'
        wrapped_key: (Optional) The encrypted ('wrapped') AES-256 key to use.
            This key should be encrypted using the Cloud KMS key specified by
            key_name.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Convert date field list to Protobuf type
    def map_fields(field: str) -> dict:
        return {"name": field}

    if date_fields:
        date_fields = map(map_fields, date_fields)
    else:
        date_fields = []

    f = []
    with open(input_csv_file) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            f.append(row)

    #  Helper function for converting CSV rows to Protobuf types
    def map_headers(header: str) -> dict:
        return {"name": header}

    def map_data(value: str) -> dict:
        try:
            date = datetime.strptime(value, "%m/%d/%Y")
            return {
                "date_value": {"year": date.year, "month": date.month, "day": date.day}
            }
        except ValueError:
            return {"string_value": value}

    def map_rows(row: str) -> dict:
        return {"values": map(map_data, row)}

    # Using the helper functions, convert CSV rows to protobuf-compatible
    # dictionaries.
    csv_headers = map(map_headers, f[0])
    csv_rows = map(map_rows, f[1:])

    # Construct the table dict
    table_item = {"table": {"headers": csv_headers, "rows": csv_rows}}

    # Construct date shift config
    date_shift_config = {
        "lower_bound_days": lower_bound_days,
        "upper_bound_days": upper_bound_days,
    }

    # If using a Cloud KMS key, add it to the date_shift_config.
    # The wrapped key is base64-encoded, but the library expects a binary
    # string, so decode it here.
    if context_field_id and key_name and wrapped_key:
        date_shift_config["context"] = {"name": context_field_id}
        date_shift_config["crypto_key"] = {
            "kms_wrapped": {
                "wrapped_key": base64.b64decode(wrapped_key),
                "crypto_key_name": key_name,
            }
        }
    elif context_field_id or key_name or wrapped_key:
        raise ValueError(
            """You must set either ALL or NONE of
        [context_field_id, key_name, wrapped_key]!"""
        )

    # Construct Deidentify Config
    deidentify_config = {
        "record_transformations": {
            "field_transformations": [
                {
                    "fields": date_fields,
                    "primitive_transformation": {
                        "date_shift_config": date_shift_config
                    },
                }
            ]
        }
    }

    # Write to CSV helper methods
    def write_header(header: types.storage.FieldId) -> str:
        return header.name

    def write_data(data: types.storage.Value) -> str:
        return data.string_value or "{}/{}/{}".format(
            data.date_value.month,
            data.date_value.day,
            data.date_value.year,
        )

    # Call the API
    response = dlp.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": deidentify_config,
            "item": table_item,
        }
    )

    # Write results to CSV file
    with open(output_csv_file, "w") as csvfile:
        write_file = csv.writer(csvfile, delimiter=",")
        write_file.writerow(map(write_header, response.item.table.headers))
        for row in response.item.table.rows:
            write_file.writerow(map(write_data, row.values))
    # Print status
    print(f"Successfully saved date-shift output to {output_csv_file}")


# [END dlp_deidentify_date_shift]


# [START dlp_deidentify_time_extract]
import csv  # noqa: F811, E402, I100
from datetime import datetime  # noqa: F811, E402, I100
from typing import List  # noqa: F811, E402

import google.cloud.dlp  # noqa: F811, E402


def deidentify_with_time_extract(
    project: str,
    date_fields: List[str],
    input_csv_file: str,
    output_csv_file: str,
) -> None:
    """Uses the Data Loss Prevention API to deidentify dates in a CSV file through
     time part extraction.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        date_fields: A list of (date) fields in CSV file to de-identify
            through time extraction. Example: ['birth_date', 'register_date'].
            Date values in format: mm/DD/YYYY are considered as part of this
            sample.
        input_csv_file: The path to the CSV file to deidentify. The first row
            of the file must specify column names, and all other rows must
            contain valid values.
        output_csv_file: The output file path to save the time extracted data.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert date field list to Protobuf type.
    def map_fields(field):
        return {"name": field}

    if date_fields:
        date_fields = map(map_fields, date_fields)
    else:
        date_fields = []

    csv_lines = []
    with open(input_csv_file) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            csv_lines.append(row)

    #  Helper function for converting CSV rows to Protobuf types
    def map_headers(header):
        return {"name": header}

    def map_data(value):
        try:
            date = datetime.strptime(value, "%m/%d/%Y")
            return {
                "date_value": {"year": date.year, "month": date.month, "day": date.day}
            }
        except ValueError:
            return {"string_value": value}

    def map_rows(row):
        return {"values": map(map_data, row)}

    # Using the helper functions, convert CSV rows to protobuf-compatible
    # dictionaries.
    csv_headers = map(map_headers, csv_lines[0])
    csv_rows = map(map_rows, csv_lines[1:])

    # Construct the table dictionary.
    table = {"headers": csv_headers, "rows": csv_rows}

    # Construct the `item` for table to de-identify.
    item = {"table": table}

    # Construct deidentify configuration dictionary.
    deidentify_config = {
        "record_transformations": {
            "field_transformations": [
                {
                    "primitive_transformation": {
                        "time_part_config": {"part_to_extract": "YEAR"}
                    },
                    "fields": date_fields,
                }
            ]
        }
    }

    # Write to CSV helper methods.
    def write_header(header):
        return header.name

    def write_data(data):
        return data.string_value or "{}/{}/{}".format(
            data.date_value.month,
            data.date_value.day,
            data.date_value.year,
        )

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API
    response = dlp.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": deidentify_config,
            "item": item,
        }
    )

    # Print the result.
    print("Table after de-identification: {}".format(response.item.table))

    # Write results to CSV file.
    with open(output_csv_file, "w") as csvfile:
        write_file = csv.writer(csvfile, delimiter=",")
        write_file.writerow(map(write_header, response.item.table.headers))
        for row in response.item.table.rows:
            write_file.writerow(map(write_data, row.values))

    # Print status.
    print(f"Successfully saved date-extracted output to {output_csv_file}")


# [END dlp_deidentify_time_extract]


# [START dlp_deidentify_replace_infotype]
from typing import List  # noqa: F811, E402, I100

import google.cloud.dlp  # noqa: F811, E402


def deidentify_with_replace_infotype(
    project: str, item: str, info_types: List[str]
) -> None:
    """Uses the Data Loss Prevention API to deidentify sensitive data in a
    string by replacing it with the info type.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        item: The string to deidentify (will be treated as text).
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Construct inspect configuration dictionary
    inspect_config = {"info_types": [{"name": info_type} for info_type in info_types]}

    # Construct deidentify configuration dictionary
    deidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {"primitive_transformation": {"replace_with_info_type_config": {}}}
            ]
        }
    }

    # Call the API
    response = dlp.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": deidentify_config,
            "inspect_config": inspect_config,
            "item": {"value": item},
        }
    )

    # Print out the results.
    print(response.item.value)


# [END dlp_deidentify_replace_infotype]


# [START dlp_deidentify_simple_word_list]
import google.cloud.dlp  # noqa: F811, E402


def deidentify_with_simple_word_list(
    project: str,
    input_str: str,
    custom_info_type_name: str,
    word_list: list[str],
) -> None:
    """Uses the Data Loss Prevention API to de-identify sensitive data in a
      string by matching against custom word list.

    Args:
        project: The Google Cloud project id to use as a parent resource.
        input_str: The string to deidentify (will be treated as text).
        custom_info_type_name: The name of the custom info type to use.
        word_list: The list of strings to match against.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Prepare custom_info_types by parsing word lists
    word_list = {"words": word_list}
    custom_info_types = [
        {
            "info_type": {"name": custom_info_type_name},
            "dictionary": {"word_list": word_list},
        }
    ]

    # Construct the configuration dictionary
    inspect_config = {
        "custom_info_types": custom_info_types,
    }

    # Construct deidentify configuration dictionary
    deidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {"primitive_transformation": {"replace_with_info_type_config": {}}}
            ]
        }
    }

    # Construct the `item`.
    item = {"value": input_str}

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API
    response = dlp.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": deidentify_config,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    print(f"De-identified Content: {response.item.value}")


# [END dlp_deidentify_simple_word_list]


# [START dlp_deidentify_exception_list]
from typing import List  # noqa: F811, E402, I100

import google.cloud.dlp  # noqa: F811, E402


def deidentify_with_exception_list(
    project: str, content_string: str, info_types: List[str], exception_list: List[str]
) -> None:
    """Uses the Data Loss Prevention API to de-identify sensitive data in a
      string but ignore matches against custom list.

    Args:
        project: The Google Cloud project id to use as a parent resource.
        content_string: The string to deidentify (will be treated as text).
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
        exception_list: The list of strings to ignore matches on.

    Returns:
          None; the response from the API is printed to the terminal.
    """

    # Instantiate a client
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct a list of infoTypes for DLP to locate in `content_string`. See
    # https://cloud.google.com/dlp/docs/concepts-infotypes for more information
    # about supported infoTypes.

    info_types = [{"name": info_type} for info_type in info_types]

    # Construct a rule set that will only match on info_type
    # if the matched text is not in the exception list.
    rule_set = [
        {
            "info_types": info_types,
            "rules": [
                {
                    "exclusion_rule": {
                        "dictionary": {"word_list": {"words": exception_list}},
                        "matching_type": google.cloud.dlp_v2.MatchingType.MATCHING_TYPE_FULL_MATCH,
                    }
                }
            ],
        }
    ]

    # Construct the configuration dictionary
    inspect_config = {
        "info_types": info_types,
        "rule_set": rule_set,
    }

    # Construct deidentify configuration dictionary
    deidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {"primitive_transformation": {"replace_with_info_type_config": {}}}
            ]
        }
    }

    # Construct the `item`.
    item = {"value": content_string}

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API
    response = dlp.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": deidentify_config,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    # Print out the results.
    print(response.item.value)


# [END dlp_deidentify_exception_list]


# [START dlp_deidentify_dictionary_replacement]
from typing import List  # noqa: F811, E402, I100

import google.cloud.dlp  # noqa: F811, E402


def deindentify_with_dictionary_replacement(
    project: str,
    input_str: str,
    info_types: List[str],
    word_list: List[str],
) -> None:
    """Uses the Data Loss Prevention API to de-identify sensitive data in a
    string by replacing each piece of detected sensitive data with a value
    that Cloud DLP randomly selects from a list of words that you provide.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        input_str: The string to deidentify (will be treated as text).
        info_types: A list of strings representing infoTypes to look for.
        word_list: List of words or phrases to search for in the data.
    """

    # Instantiate a client
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct list of info types
    info_types = [{"name": info_type} for info_type in info_types]

    # Construct deidentify configuration dictionary
    deidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {
                    "info_types": info_types,
                    "primitive_transformation": {
                        "replace_dictionary_config": {"word_list": {"words": word_list}}
                    },
                }
            ]
        }
    }

    # Construct the `item`
    item = {"value": input_str}

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API
    response = dlp.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": deidentify_config,
            "inspect_config": {"info_types": info_types},
            "item": item,
        }
    )

    # Print out the results.
    print(f"De-identified Content: {response.item.value}")


# [END dlp_deidentify_dictionary_replacement]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(
        dest="content", help="Select how to submit content to the API."
    )
    subparsers.required = True

    mask_parser = subparsers.add_parser(
        "deid_mask",
        help="Deidentify sensitive data in a string by masking it with a " "character.",
    )
    mask_parser.add_argument(
        "--info_types",
        nargs="+",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
        "If unspecified, the three above examples will be used.",
        default=["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"],
    )
    mask_parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    mask_parser.add_argument("item", help="The string to deidentify.")
    mask_parser.add_argument(
        "-n",
        "--number_to_mask",
        type=int,
        default=0,
        help="The maximum number of sensitive characters to mask in a match. "
        "If omitted the request or set to 0, the API will mask any mathcing "
        "characters.",
    )
    mask_parser.add_argument(
        "-m",
        "--masking_character",
        help="The character to mask matching sensitive data with.",
    )

    replace_parser = subparsers.add_parser(
        "deid_replace",
        help="Deidentify sensitive data in a string by replacing it with "
        "another string.",
    )
    replace_parser.add_argument(
        "--info_types",
        nargs="+",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
        "If unspecified, the three above examples will be used.",
        default=["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"],
    )
    replace_parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    replace_parser.add_argument("item", help="The string to deidentify.")
    replace_parser.add_argument(
        "replacement_str", help="The string to " "replace all matched values with."
    )

    fpe_parser = subparsers.add_parser(
        "deid_fpe",
        help="Deidentify sensitive data in a string using Format Preserving "
        "Encryption (FPE).",
    )
    fpe_parser.add_argument(
        "--info_types",
        action="append",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
        "If unspecified, the three above examples will be used.",
        default=["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"],
    )
    fpe_parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    fpe_parser.add_argument(
        "item",
        help="The string to deidentify. " "Example: string = 'My SSN is 372819127'",
    )
    fpe_parser.add_argument(
        "key_name",
        help="The name of the Cloud KMS key used to encrypt ('wrap') the "
        "AES-256 key. Example: "
        "key_name = 'projects/YOUR_GCLOUD_PROJECT/locations/YOUR_LOCATION/"
        "keyRings/YOUR_KEYRING_NAME/cryptoKeys/YOUR_KEY_NAME'",
    )
    fpe_parser.add_argument(
        "wrapped_key",
        help="The encrypted ('wrapped') AES-256 key to use. This key should "
        "be encrypted using the Cloud KMS key specified by key_name.",
    )
    fpe_parser.add_argument(
        "-a",
        "--alphabet",
        default="ALPHA_NUMERIC",
        help="The set of characters to replace sensitive ones with. Commonly "
        'used subsets of the alphabet include "NUMERIC", "HEXADECIMAL", '
        '"UPPER_CASE_ALPHA_NUMERIC", "ALPHA_NUMERIC", '
        '"FFX_COMMON_NATIVE_ALPHABET_UNSPECIFIED"',
    )
    fpe_parser.add_argument(
        "-s",
        "--surrogate_type",
        help="The name of the surrogate custom info type to use. Only "
        "necessary if you want to reverse the deidentification process. Can "
        "be essentially any arbitrary string, as long as it doesn't appear "
        "in your dataset otherwise.",
    )

    reid_parser = subparsers.add_parser(
        "reid_fpe",
        help="Reidentify sensitive data in a string using Format Preserving "
        "Encryption (FPE).",
    )
    reid_parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    reid_parser.add_argument(
        "item",
        help="The string to deidentify. " "Example: string = 'My SSN is 372819127'",
    )
    reid_parser.add_argument(
        "surrogate_type",
        help="The name of the surrogate custom info type to use. Only "
        "necessary if you want to reverse the deidentification process. Can "
        "be essentially any arbitrary string, as long as it doesn't appear "
        "in your dataset otherwise.",
    )
    reid_parser.add_argument(
        "key_name",
        help="The name of the Cloud KMS key used to encrypt ('wrap') the "
        "AES-256 key. Example: "
        "key_name = 'projects/YOUR_GCLOUD_PROJECT/locations/YOUR_LOCATION/"
        "keyRings/YOUR_KEYRING_NAME/cryptoKeys/YOUR_KEY_NAME'",
    )
    reid_parser.add_argument(
        "wrapped_key",
        help="The encrypted ('wrapped') AES-256 key to use. This key should "
        "be encrypted using the Cloud KMS key specified by key_name.",
    )
    reid_parser.add_argument(
        "-a",
        "--alphabet",
        default="ALPHA_NUMERIC",
        help="The set of characters to replace sensitive ones with. Commonly "
        'used subsets of the alphabet include "NUMERIC", "HEXADECIMAL", '
        '"UPPER_CASE_ALPHA_NUMERIC", "ALPHA_NUMERIC", '
        '"FFX_COMMON_NATIVE_ALPHABET_UNSPECIFIED"',
    )

    date_shift_parser = subparsers.add_parser(
        "deid_date_shift",
        help="Deidentify dates in a CSV file by pseudorandomly shifting them.",
    )
    date_shift_parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    date_shift_parser.add_argument(
        "input_csv_file",
        help="The path to the CSV file to deidentify. The first row of the "
        "file must specify column names, and all other rows must contain "
        "valid values.",
    )
    date_shift_parser.add_argument(
        "output_csv_file", help="The path to save the date-shifted CSV file."
    )
    date_shift_parser.add_argument(
        "lower_bound_days",
        type=int,
        help="The maximum number of days to shift a date backward",
    )
    date_shift_parser.add_argument(
        "upper_bound_days",
        type=int,
        help="The maximum number of days to shift a date forward",
    )
    date_shift_parser.add_argument(
        "date_fields",
        nargs="+",
        help="The list of date fields in the CSV file to date shift. Example: "
        "['birth_date', 'register_date']",
    )
    date_shift_parser.add_argument(
        "--context_field_id",
        help="(Optional) The column to determine date shift amount based on. "
        "If this is not specified, a random shift amount will be used for "
        "every row. If this is specified, then 'wrappedKey' and 'keyName' "
        "must also be set.",
    )
    date_shift_parser.add_argument(
        "--key_name",
        help="(Optional) The name of the Cloud KMS key used to encrypt "
        "('wrap') the AES-256 key. Example: "
        "key_name = 'projects/YOUR_GCLOUD_PROJECT/locations/YOUR_LOCATION/"
        "keyRings/YOUR_KEYRING_NAME/cryptoKeys/YOUR_KEY_NAME'",
    )
    date_shift_parser.add_argument(
        "--wrapped_key",
        help="(Optional) The encrypted ('wrapped') AES-256 key to use. This "
        "key should be encrypted using the Cloud KMS key specified by"
        "key_name.",
    )

    time_extract_parser = subparsers.add_parser(
        "deid_time_extract",
        help="Deidentify dates in a CSV file by extracting a date part.",
    )
    time_extract_parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    time_extract_parser.add_argument(
        "input_csv_file",
        help="The path to the CSV file to deidentify. The first row of the "
        "file must specify column names, and all other rows must contain "
        "valid values.",
    )
    time_extract_parser.add_argument(
        "date_fields",
        nargs="+",
        help="The list of date fields in the CSV file to de-identify. Example: "
        "['birth_date', 'register_date']",
    )
    time_extract_parser.add_argument(
        "output_csv_file", help="The path to save the time-extracted data."
    )

    replace_with_infotype_parser = subparsers.add_parser(
        "replace_with_infotype",
        help="Deidentify sensitive data in a string by replacing it with the "
        "info type of the data.",
    )
    replace_with_infotype_parser.add_argument(
        "--info_types",
        action="append",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
        "If unspecified, the three above examples will be used.",
        default=["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"],
    )
    replace_with_infotype_parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    replace_with_infotype_parser.add_argument(
        "item",
        help="The string to deidentify."
        "Example: 'My credit card is 4242 4242 4242 4242'",
    )

    deid_word_list_parser = subparsers.add_parser(
        "deid_simple_word_list",
        help="Deidentify sensitive data in a string against a custom simple word list",
    )
    deid_word_list_parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    deid_word_list_parser.add_argument(
        "input_str",
        help="The string to deidentify.",
    )
    deid_word_list_parser.add_argument(
        "custom_info_type_name",
        help="The name of the custom info type to use.",
    )
    deid_word_list_parser.add_argument(
        "word_list",
        help="The list of strings to match against.",
    )

    deid_exception_list_parser = subparsers.add_parser(
        "deid_exception_list",
        help="De-identify sensitive data in a string , ignore matches against a custom word list",
    )
    deid_exception_list_parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    deid_exception_list_parser.add_argument(
        "content_string",
        help="The string to de-identify.",
    )
    deid_exception_list_parser.add_argument(
        "--info_types",
        nargs="+",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". ',
    )
    deid_exception_list_parser.add_argument(
        "exception_list",
        help="The list of strings to ignore matches against.",
    )

    replace_from_dictionary_parser = subparsers.add_parser(
        "dictionary_replacement",
        help="De-identify sensitive data in a string by replacing it with a "
        "random value from a custom word list.",
    )
    replace_from_dictionary_parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    replace_from_dictionary_parser.add_argument(
        "--info_types",
        action="append",
        help="Strings representing infoTypes to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". ',
    )
    replace_from_dictionary_parser.add_argument(
        "input_str",
        help="The string to de-identify.",
    )
    replace_from_dictionary_parser.add_argument(
        "word_list", help="List of words or phrases to search for in the data."
    )

    args = parser.parse_args()

    if args.content == "deid_mask":
        deidentify_with_mask(
            args.project,
            args.item,
            args.info_types,
            masking_character=args.masking_character,
            number_to_mask=args.number_to_mask,
        )
    elif args.content == "deid_replace":
        deidentify_with_replace(
            args.project,
            args.item,
            args.info_types,
            replacement_str=args.replacement_str,
        )
    elif args.content == "deid_fpe":
        deidentify_with_fpe(
            args.project,
            args.item,
            args.info_types,
            alphabet=args.alphabet,
            wrapped_key=args.wrapped_key,
            key_name=args.key_name,
            surrogate_type=args.surrogate_type,
        )
    elif args.content == "reid_text_fpe":
        reidentify_text_with_fpe(
            args.project,
            args.item,
            wrapped_key=args.wrapped_key,
            key_name=args.key_name,
        )
    elif args.content == "reid_fpe":
        reidentify_with_fpe(
            args.project,
            args.item,
            surrogate_type=args.surrogate_type,
            wrapped_key=args.wrapped_key,
            key_name=args.key_name,
            alphabet=args.alphabet,
        )
    elif args.content == "deid_date_shift":
        deidentify_with_date_shift(
            args.project,
            input_csv_file=args.input_csv_file,
            output_csv_file=args.output_csv_file,
            lower_bound_days=args.lower_bound_days,
            upper_bound_days=args.upper_bound_days,
            date_fields=args.date_fields,
            context_field_id=args.context_field_id,
            wrapped_key=args.wrapped_key,
            key_name=args.key_name,
        )
    elif args.content == "deid_time_extract":
        deidentify_with_time_extract(
            args.project,
            date_fields=args.date_fields,
            input_csv_file=args.input_csv_file,
            output_csv_file=args.output_csv_file,
        )
    elif args.content == "replace_with_infotype":
        deidentify_with_replace_infotype(
            args.project,
            item=args.item,
            info_types=args.info_types,
        )
    elif args.content == "deid_simple_word_list":
        deidentify_with_simple_word_list(
            args.project,
            args.input_str,
            args.custom_info_type_name,
            args.word_list,
        )
    elif args.content == "deid_exception_list":
        deidentify_with_exception_list(
            args.project,
            args.content_string,
            args.info_types,
            args.exception_list,
        )
    elif args.content == "dictionary_replacement":
        deindentify_with_dictionary_replacement(
            args.project,
            args.input_str,
            args.info_types,
            args.word_list,
        )
