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
from typing import List  # noqa: F811, E402, I100

import google.cloud.dlp  # noqa: F811, E402


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
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.deidentify_content(
        request={"parent": parent, "deidentify_config": deidentify_config, "item": item}
    )

    # Print out results.
    print(f"Table after de-identification: {response.item.table}")


# [END dlp_deidentify_table_fpe]


# [START dlp_reidentify_table_fpe]
from typing import List  # noqa: F811, E402, I100

import google.cloud.dlp  # noqa: F811, E402


def reidentify_table_with_fpe(
    project: str,
    table_header: List[str],
    table_rows: List[List[str]],
    reid_field_names: List[str],
    key_name: str = None,
    wrapped_key: bytes = None,
    alphabet: str = None,
) -> None:
    """Uses the Data Loss Prevention API to re-identify sensitive data in a
    table that was encrypted by Format Preserving Encryption (FPE).

    Args:
        project: The Google Cloud project id to use as a parent resource.
        table_header: List of strings representing table field names.
        table_rows: List of rows representing table data.
        reid_field_names: A list of fields in table to re-identify.
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

    # Convert table to `item`
    item = {"table": table}

    # Specify fields to be re-identified/decrypted.
    reid_field_names = [{"name": _i} for _i in reid_field_names]

    # Construct FPE configuration dictionary
    crypto_replace_ffx_fpe_config = {
        "crypto_key": {
            "kms_wrapped": {"wrapped_key": wrapped_key, "crypto_key_name": key_name}
        },
        "common_alphabet": alphabet,
    }

    # Construct reidentify configuration dictionary
    reidentify_config = {
        "record_transformations": {
            "field_transformations": [
                {
                    "primitive_transformation": {
                        "crypto_replace_ffx_fpe_config": crypto_replace_ffx_fpe_config,
                    },
                    "fields": reid_field_names,
                }
            ]
        }
    }

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.reidentify_content(
        request={
            "parent": parent,
            "reidentify_config": reidentify_config,
            "item": item,
        }
    )

    # Print out results.
    print("Table after re-identification: {}".format(response.item.table))


# [END dlp_reidentify_table_fpe]


# [START dlp_deidentify_table_with_crypto_hash]
from typing import Dict, List, Union  # noqa: F811, E402, I100

import google.cloud.dlp  # noqa: F811, E402


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
    parent = f"projects/{project}"

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
    print("Table after de-identification: {}".format(response.item.table))


# [END dlp_deidentify_table_with_crypto_hash]


# [START dlp_deidentify_table_with_multiple_crypto_hash]
from typing import Dict, List, Union  # noqa: F811, E402, I100

import google.cloud.dlp  # noqa: F811, E402


def deidentify_table_with_multiple_crypto_hash(
    project: str,
    table_data: Dict[str, Union[List[str], List[List[str]]]],
    info_types: List[str],
    transient_key_name_1: str,
    transient_key_name_2: str,
    deid_fields_1: List[str],
    deid_fields_2: List[str],
) -> None:
    """Uses the Data Loss Prevention API to de-identify sensitive data
    in table using multiple transient cryptographic hash keys.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        table_data: Dictionary representing table data.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
        transient_key_name_1: Name of the first transient crypto key used
            for encryption. The scope of this key is a single API call.
            It is generated for the transformation and then discarded.
        transient_key_name_2: Name of the second transient crypto key used
            for encryption. The scope of this key is a single API call.
            It is generated for the transformation and then discarded.
        deid_fields_1: List of column names in table to de-identify using
            transient_key_name_1.
        deid_fields_2: List of column names in table to de-identify using
            transient_key_name_2.

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

    # Construct the `item`
    item = {"table": table}

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries.
    info_types = [{"name": info_type} for info_type in info_types]

    # Construct cryptographic hash configurations using two transient keys
    # which will encrypt the data.
    crypto_hash_config_1 = {"crypto_key": {"transient": {"name": transient_key_name_1}}}
    crypto_hash_config_2 = {"crypto_key": {"transient": {"name": transient_key_name_2}}}

    # Prepare fields to be de-identified by converting list of strings
    # into list of dictionaries.
    deid_fields_1 = [{"name": field} for field in deid_fields_1]
    deid_fields_2 = [{"name": field} for field in deid_fields_2]

    # Specify the type of info the inspection will look for.
    inspect_config = {
        "info_types": info_types,
    }

    # Construct deidentify configuration dictionary.
    deidentify_config = {
        "record_transformations": {
            "field_transformations": [
                {
                    "fields": deid_fields_1,
                    "primitive_transformation": {
                        "crypto_hash_config": crypto_hash_config_1
                    },
                },
                {
                    "fields": deid_fields_2,
                    "info_type_transformations": {
                        "transformations": [
                            {
                                "info_types": info_types,
                                "primitive_transformation": {
                                    "crypto_hash_config": crypto_hash_config_2
                                },
                            }
                        ]
                    },
                },
            ]
        }
    }

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

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
    print("Table after de-identification: {}".format(response.item.table))


# [END dlp_deidentify_table_with_multiple_crypto_hash]

# [START dlp_deidentify_table_bucketing]
from typing import Dict, List, Union  # noqa: F811, E402, I100

import google.cloud.dlp  # noqa: F811, E402
from google.cloud.dlp_v2 import types  # noqa: F811, E402


def deidentify_table_bucketing(
    project: str,
    table_data: Dict[str, Union[List[str], List[List[str]]]],
    deid_content_list: List[str],
    bucket_size: int,
    bucketing_lower_bound: int,
    bucketing_upper_bound: int,
) -> types.dlp.Table:
    """Uses the Data Loss Prevention API to de-identify sensitive data in a
    table by replacing them with fixed size bucket ranges.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        table_data: Dictionary representing table data.
        deid_content_list: A list of fields in table to de-identify.
        bucket_size: Size of each bucket for fixed sized bucketing
            (except for minimum and maximum buckets). So if ``bucketing_lower_bound`` = 10,
            ``bucketing_upper_bound`` = 89, and ``bucket_size`` = 10, then the
            following buckets would be used: -10, 10-20, 20-30, 30-40,
            40-50, 50-60, 60-70, 70-80, 80-89, 89+.
       bucketing_lower_bound: Lower bound value of buckets.
       bucketing_upper_bound:  Upper bound value of buckets.

    Returns:
       De-identified table is returned;
       the response from the API is also printed to the terminal.

    Example:
    >> $ python deid.py deid_table_bucketing \
        '{"header": ["email", "phone number", "age"],
        "rows": [["robertfrost@example.com", "4232342345", "35"],
        ["johndoe@example.com", "4253458383", "68"]]}' \
        ["age"] 10 0 100
        >>  '{"header": ["email", "phone number", "age"],
            "rows": [["robertfrost@example.com", "4232342345", "30:40"],
            ["johndoe@example.com", "4253458383", "60:70"]]}'
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Construct the `table`. For more details on the table schema, please see
    # https://cloud.google.com/dlp/docs/reference/rest/v2/ContentItem#Table
    headers = [{"name": val} for val in table_data["header"]]
    rows = []
    for row in table_data["rows"]:
        rows.append({"values": [{"string_value": cell_val} for cell_val in row]})

    table = {"headers": headers, "rows": rows}

    # Construct the `item`.
    item = {"table": table}

    # Construct fixed sized bucketing configuration
    fixed_size_bucketing_config = {
        "bucket_size": bucket_size,
        "lower_bound": {"integer_value": bucketing_lower_bound},
        "upper_bound": {"integer_value": bucketing_upper_bound},
    }

    # Specify fields to be de-identified
    deid_content_list = [{"name": _i} for _i in deid_content_list]

    # Construct Deidentify Config
    deidentify_config = {
        "record_transformations": {
            "field_transformations": [
                {
                    "fields": deid_content_list,
                    "primitive_transformation": {
                        "fixed_size_bucketing_config": fixed_size_bucketing_config
                    },
                }
            ]
        }
    }

    # Call the API.
    response = dlp.deidentify_content(
        request={"parent": parent, "deidentify_config": deidentify_config, "item": item}
    )

    # Print the results.
    print(f"Table after de-identification: {response.item.table}")

    # Return the response.
    return response.item.table


# [END dlp_deidentify_table_bucketing]


# [START dlp_deidentify_table_primitive_bucketing]
import google.cloud.dlp  # noqa: F811, E402, I100


def deidentify_table_primitive_bucketing(
    project: str,
) -> None:
    """ Uses the Data Loss Prevention API to de-identify sensitive data in
    a table by replacing them with generalized bucket labels.
    Args:
        project: The Google Cloud project id to use as a parent resource.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Dictionary representing table to de-identify.
    # The table can also be taken as input to the function.
    table_to_deid = {
        "header": ["age", "patient", "happiness_score"],
        "rows": [
            ["101", "Charles Dickens", "95"],
            ["22", "Jane Austen", "21"],
            ["90", "Mark Twain", "75"],
        ],
    }

    # Construct the `table`. For more details on the table schema, please see
    # https://cloud.google.com/dlp/docs/reference/rest/v2/ContentItem#Table
    headers = [{"name": val} for val in table_to_deid["header"]]
    rows = []
    for row in table_to_deid["rows"]:
        rows.append({"values": [{"string_value": cell_val} for cell_val in row]})

    table = {"headers": headers, "rows": rows}

    # Construct the `item` for table to de-identify.
    item = {"table": table}

    # Construct generalised bucket configuration.
    buckets_config = [
        {"min_": {"integer_value": 0}, "max_": {"integer_value": 25}, "replacement_value": {"string_value": "Low"}},
        {"min_": {"integer_value": 25}, "max_": {"integer_value": 75}, "replacement_value": {"string_value": "Medium"}},
        {"min_": {"integer_value": 75}, "max_": {"integer_value": 100}, "replacement_value": {"string_value": "High"}},
    ]

    # Construct de-identify configuration that groups values in a table field and replace those with bucket labels.
    deidentify_config = {
        "record_transformations": {
            "field_transformations": [
                {
                    "fields": [{"name": "happiness_score"}],
                    "primitive_transformation": {
                        "bucketing_config": {"buckets": buckets_config}
                    }
                }
            ]
        }
    }

    # Call the API to deidentify table data through primitive bucketing.
    response = dlp.deidentify_content(request={
        "parent": parent,
        "deidentify_config": deidentify_config,
        "item": item,
    })

    # Print the results.
    print("Table after de-identification: {}".format(response.item.table))


# [END dlp_deidentify_table_primitive_bucketing]


# [START dlp_deidentify_table_condition_infotypes]
from typing import Dict, List, Union  # noqa: F811, E402, I100

import google.cloud.dlp  # noqa: F811, E402
from google.cloud.dlp_v2 import types  # noqa: F811, E402


def deidentify_table_condition_replace_with_info_types(
    project: str,
    table_data: Dict[str, Union[List[str], List[List[str]]]],
    deid_content_list: List[str],
    info_types: List[str],
    condition_field: str = None,
    condition_operator: str = None,
    condition_value: int = None,
) -> types.dlp.Table:
    """Uses the Data Loss Prevention API to de-identify sensitive data in a
    table by replacing them with info-types based on a condition.
    Args:
       project: The Google Cloud project id to use as a parent resource.
       table_data: Json string representing table data.
       deid_content_list: A list of fields in table to de-identify.
       info_types: A list of strings representing info types to look for.
           A full list of info categories and types is available from the API.
           Examples include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
       condition_field: A table field within the record this condition is evaluated against.
       condition_operator: Operator used to compare the field or infoType to the value. One of:
           RELATIONAL_OPERATOR_UNSPECIFIED, EQUAL_TO, NOT_EQUAL_TO, GREATER_THAN, LESS_THAN, GREATER_THAN_OR_EQUALS,
           LESS_THAN_OR_EQUALS, EXISTS.
       condition_value: Value to compare against. [Mandatory, except for ``EXISTS`` tests.].

    Returns:
       De-identified table is returned;
       the response from the API is also printed to the terminal.

    Example:
    >> $ python deid.py deid_table_condition_replace \
    '{"header": ["email", "phone number", "age"],
    "rows": [["robertfrost@example.com", "4232342345", "45"],
    ["johndoe@example.com", "4253458383", "63"]]}' ["email"] \
    ["EMAIL_ADDRESS"] "age" "GREATER_THAN" 50
    >> '{"header": ["email", "phone number", "age"],
        "rows": [["robertfrost@example.com", "4232342345", "45"],
        ["[EMAIL_ADDRESS]", "4253458383", "63"]]}'
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

    # Construct the item
    item = {"table": table}

    # Specify fields to be de-identified
    deid_field_list = [{"name": _i} for _i in deid_content_list]

    # Construct inspect configuration dictionary
    inspect_config = {"info_types": [{"name": info_type} for info_type in info_types]}

    # Construct condition list
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
            "field_transformations": [
                {
                    "info_type_transformations": {
                        "transformations": [
                            {
                                "primitive_transformation": {
                                    "replace_with_info_type_config": {}
                                }
                            }
                        ]
                    },
                    "fields": deid_field_list,
                    "condition": {
                        "expressions": {"conditions": {"conditions": condition}}
                    },
                }
            ]
        }
    }

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": deidentify_config,
            "item": item,
            "inspect_config": inspect_config,
        }
    )

    print(f"Table after de-identification: {response.item.table}")

    return response.item.table


# [END dlp_deidentify_table_condition_infotypes]


# [START dlp_deidentify_table_condition_masking]
from typing import Dict, List, Union  # noqa: F811, E402, I100

import google.cloud.dlp  # noqa: F811, E402
from google.cloud.dlp_v2 import types  # noqa: F811, E402


def deidentify_table_condition_masking(
    project: str,
    table_data: Dict[str, Union[List[str], List[List[str]]]],
    deid_content_list: List[str],
    condition_field: str = None,
    condition_operator: str = None,
    condition_value: int = None,
    masking_character: str = None,
) -> types.dlp.Table:
    """ Uses the Data Loss Prevention API to de-identify sensitive data in a
      table by masking them based on a condition.

    Args:
        project: The Google Cloud project id to use as a parent resource.
        table_data: Json string representing table data.
        deid_content_list: A list of fields in table to de-identify.
        condition_field: A table Field within the record this condition is evaluated against.
        condition_operator: Operator used to compare the field or infoType to the value. One of:
            RELATIONAL_OPERATOR_UNSPECIFIED, EQUAL_TO, NOT_EQUAL_TO, GREATER_THAN, LESS_THAN, GREATER_THAN_OR_EQUALS,
            LESS_THAN_OR_EQUALS, EXISTS.
        condition_value: Value to compare against. [Mandatory, except for ``EXISTS`` tests.].
        masking_character: The character to mask matching sensitive data with.

    Returns:
        De-identified table is returned;
        the response from the API is also printed to the terminal.

    Example:
    >> $ python deid.py deid_table_condition_mask \
    '{"header": ["email", "phone number", "age", "happiness_score"],
    "rows": [["robertfrost@example.com", "4232342345", "35", "21"],
    ["johndoe@example.com", "4253458383", "64", "34"]]}' \
    ["happiness_score"] "age" "GREATER_THAN" 50
    >> '{"header": ["email", "phone number", "age", "happiness_score"],
        "rows": [["robertfrost@example.com", "4232342345", "35", "21"],
        ["johndoe@example.com", "4253458383", "64", "**"]]}'
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

    # Construct the `item`
    item = {"table": table}

    # Specify fields to be de-identified
    deid_content_list = [{"name": _i} for _i in deid_content_list]

    # Construct condition list
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
            "field_transformations": [
                {
                    "primitive_transformation": {
                        "character_mask_config": {
                            "masking_character": masking_character
                        }
                    },
                    "fields": deid_content_list,
                    "condition": {
                        "expressions": {"conditions": {"conditions": condition}}
                    },
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

    # Print the result
    print(f"Table after de-identification: {response.item.table}")

    # Return the response
    return response.item.table


# [END dlp_deidentify_table_condition_masking]


# [START dlp_deidentify_table_infotypes]
from typing import Dict, List, Union  # noqa: F811, E402, I100

import google.cloud.dlp  # noqa: F811, E402


def deidentify_table_replace_with_info_types(
    project: str,
    table_data: Dict[str, Union[List[str], List[List[str]]]],
    info_types: List[str],
    deid_content_list: List[str],
) -> None:
    """ Uses the Data Loss Prevention API to de-identify sensitive data in a
      table by replacing them with info type.

    Args:
        project: The Google Cloud project id to use as a parent resource.
        table_data: Json string representing table data.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
        deid_content_list: A list of fields in table to de-identify

    Returns:
        None; the response from the API is printed to the terminal.

    Example:
    >> $ python deid.py table_replace_with_infotype \
    '{
        "header": ["name", "email", "phone number"],
        "rows": [
            ["Robert Frost", "robertfrost@example.com", "4232342345"],
            ["John Doe", "johndoe@example.com", "4253458383"]
        ]
    }' \
    ["PERSON_NAME"] ["name"]
    >> '{
            "header": ["name", "email", "phone number"],
            "rows": [
                ["[PERSON_NAME]", "robertfrost@example.com", "4232342345"],
                ["[PERSON_NAME]", "johndoe@example.com", "4253458383"]
            ]
        }'
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

    # Construct item
    item = {"table": table}

    # Specify fields to be de-identified
    deid_content_list = [{"name": _i} for _i in deid_content_list]

    # Construct inspect configuration dictionary
    inspect_config = {"info_types": [{"name": info_type} for info_type in info_types]}

    # Construct deidentify configuration dictionary
    deidentify_config = {
        "record_transformations": {
            "field_transformations": [
                {
                    "info_type_transformations": {
                        "transformations": [
                            {
                                "primitive_transformation": {
                                    "replace_with_info_type_config": {}
                                }
                            }
                        ]
                    },
                    "fields": deid_content_list,
                }
            ]
        }
    }

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": deidentify_config,
            "item": item,
            "inspect_config": inspect_config,
        }
    )

    # Print the result
    print(f"Table after de-identification: {response.item.table}")


# [END dlp_deidentify_table_infotypes]

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
