# Copyright 2017 Google Inc.
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

from __future__ import print_function

import argparse


# [START dlp_deidentify_masking]
def deidentify_with_mask(project, string, info_types, masking_character=None,
                         number_to_mask=0):
    """Uses the Data Loss Prevention API to deidentify sensitive data in a
    string by masking it with a character.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        item: The string to deidentify (will be treated as text).
        masking_character: The character to mask matching sensitive data with.
        number_to_mask: The maximum number of sensitive characters to mask in
            a match. If omitted or set to zero, the API will default to no
            maximum.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Import the client library
    import google.cloud.dlp

    # Instantiate a client
    dlp = google.cloud.dlp.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = dlp.project_path(project)

    # Construct inspect configuration dictionary
    inspect_config = {
        'info_types': [{'name': info_type} for info_type in info_types]
    }

    # Construct deidentify configuration dictionary
    deidentify_config = {
        'info_type_transformations': {
            'transformations': [
                {
                    'primitive_transformation': {
                        'character_mask_config': {
                            'masking_character': masking_character,
                            'number_to_mask': number_to_mask
                        }
                    }
                }
            ]
        }
    }

    # Construct item
    item = {'value': string}

    # Call the API
    response = dlp.deidentify_content(
        parent, inspect_config=inspect_config,
        deidentify_config=deidentify_config, item=item)

    # Print out the results.
    print(response.item.value)
# [END dlp_deidentify_masking]


# [START dlp_deidentify_fpe]
def deidentify_with_fpe(project, string, info_types, alphabet=None,
                        surrogate_type=None, key_name=None, wrapped_key=None):
    """Uses the Data Loss Prevention API to deidentify sensitive data in a
    string using Format Preserving Encryption (FPE).
    Args:
        project: The Google Cloud project id to use as a parent resource.
        item: The string to deidentify (will be treated as text).
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
    # Import the client library
    import google.cloud.dlp

    # Instantiate a client
    dlp = google.cloud.dlp.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = dlp.project_path(project)

    # The wrapped key is base64-encoded, but the library expects a binary
    # string, so decode it here.
    import base64
    wrapped_key = base64.b64decode(wrapped_key)

    # Construct FPE configuration dictionary
    crypto_replace_ffx_fpe_config = {
        'crypto_key': {
            'kms_wrapped': {
                'wrapped_key': wrapped_key,
                'crypto_key_name': key_name
            }
        },
        'common_alphabet': alphabet
    }

    # Add surrogate type
    if surrogate_type:
        crypto_replace_ffx_fpe_config['surrogate_info_type'] = {
            'name': surrogate_type
        }

    # Construct inspect configuration dictionary
    inspect_config = {
        'info_types': [{'name': info_type} for info_type in info_types]
    }

    # Construct deidentify configuration dictionary
    deidentify_config = {
        'info_type_transformations': {
            'transformations': [
                {
                    'primitive_transformation': {
                        'crypto_replace_ffx_fpe_config':
                            crypto_replace_ffx_fpe_config
                    }
                }
            ]
        }
    }

    # Convert string to item
    item = {'value': string}

    # Call the API
    response = dlp.deidentify_content(
        parent, inspect_config=inspect_config,
        deidentify_config=deidentify_config, item=item)

    # Print results
    print(response.item.value)
# [END dlp_deidentify_fpe]


# [START dlp_reidentify_fpe]
def reidentify_with_fpe(project, string, alphabet=None,
                        surrogate_type=None, key_name=None, wrapped_key=None):
    """Uses the Data Loss Prevention API to reidentify sensitive data in a
    string that was encrypted by Format Preserving Encryption (FPE).
    Args:
        project: The Google Cloud project id to use as a parent resource.
        item: The string to deidentify (will be treated as text).
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
    # Import the client library
    import google.cloud.dlp

    # Instantiate a client
    dlp = google.cloud.dlp.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = dlp.project_path(project)

    # The wrapped key is base64-encoded, but the library expects a binary
    # string, so decode it here.
    import base64
    wrapped_key = base64.b64decode(wrapped_key)

    # Construct Deidentify Config
    reidentify_config = {
        'info_type_transformations': {
            'transformations': [
                {
                    'primitive_transformation': {
                        'crypto_replace_ffx_fpe_config': {
                            'crypto_key': {
                                'kms_wrapped': {
                                    'wrapped_key': wrapped_key,
                                    'crypto_key_name': key_name
                                }
                            },
                            'common_alphabet': alphabet,
                            'surrogate_info_type': {
                                'name': surrogate_type
                            }
                        }
                    }
                }
            ]
        }
    }

    inspect_config = {
        'custom_info_types': [
            {
                'info_type': {
                    'name': surrogate_type
                },
                'surrogate_type': {
                }
            }
        ]
    }

    # Convert string to item
    item = {'value': string}

    # Call the API
    response = dlp.reidentify_content(
        parent,
        inspect_config=inspect_config,
        reidentify_config=reidentify_config,
        item=item)

    # Print results
    print(response.item.value)
# [END dlp_reidentify_fpe]


# [START dlp_deidentify_date_shift]
def deidentify_with_date_shift(project, input_csv_file=None,
                               output_csv_file=None, date_fields=None,
                               lower_bound_days=None, upper_bound_days=None,
                               context_field_id=None, wrapped_key=None,
                               key_name=None):
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
    # Import the client library
    import google.cloud.dlp

    # Instantiate a client
    dlp = google.cloud.dlp.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = dlp.project_path(project)

    # Convert date field list to Protobuf type
    def map_fields(field):
        return {'name': field}

    if date_fields:
        date_fields = map(map_fields, date_fields)
    else:
        date_fields = []

    # Read and parse the CSV file
    import csv
    from datetime import datetime
    f = []
    with open(input_csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            f.append(row)

    #  Helper function for converting CSV rows to Protobuf types
    def map_headers(header):
        return {'name': header}

    def map_data(value):
        try:
            date = datetime.strptime(value, '%m/%d/%Y')
            return {
                'date_value': {
                    'year': date.year,
                    'month': date.month,
                    'day': date.day
                }
            }
        except ValueError:
            return {'string_value': value}

    def map_rows(row):
        return {'values': map(map_data, row)}

    # Using the helper functions, convert CSV rows to protobuf-compatible
    # dictionaries.
    csv_headers = map(map_headers, f[0])
    csv_rows = map(map_rows, f[1:])

    # Construct the table dict
    table_item = {
        'table': {
            'headers': csv_headers,
            'rows': csv_rows
        }
    }

    # Construct date shift config
    date_shift_config = {
        'lower_bound_days': lower_bound_days,
        'upper_bound_days': upper_bound_days
    }

    # If using a Cloud KMS key, add it to the date_shift_config.
    # The wrapped key is base64-encoded, but the library expects a binary
    # string, so decode it here.
    if context_field_id and key_name and wrapped_key:
        import base64
        date_shift_config['context'] = {'name': context_field_id}
        date_shift_config['crypto_key'] = {
            'kms_wrapped': {
                'wrapped_key': base64.b64decode(wrapped_key),
                'crypto_key_name': key_name
            }
        }
    elif context_field_id or key_name or wrapped_key:
        raise ValueError("""You must set either ALL or NONE of
        [context_field_id, key_name, wrapped_key]!""")

    # Construct Deidentify Config
    deidentify_config = {
        'record_transformations': {
            'field_transformations': [
                {
                    'fields': date_fields,
                    'primitive_transformation': {
                        'date_shift_config': date_shift_config
                    }
                }
            ]
        }
    }

    # Write to CSV helper methods
    def write_header(header):
        return header.name

    def write_data(data):
        return data.string_value or '%s/%s/%s' % (data.date_value.month,
                                                  data.date_value.day,
                                                  data.date_value.year)

    # Call the API
    response = dlp.deidentify_content(
        parent, deidentify_config=deidentify_config, item=table_item)

    # Write results to CSV file
    with open(output_csv_file, 'w') as csvfile:
        write_file = csv.writer(csvfile, delimiter=',')
        write_file.writerow(map(write_header, response.item.table.headers))
        for row in response.item.table.rows:
            write_file.writerow(map(write_data, row.values))
    # Print status
    print('Successfully saved date-shift output to {}'.format(
                output_csv_file))
# [END dlp_deidentify_date_shift]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(
        dest='content', help='Select how to submit content to the API.')
    subparsers.required = True

    mask_parser = subparsers.add_parser(
        'deid_mask',
        help='Deidentify sensitive data in a string by masking it with a '
             'character.')
    mask_parser.add_argument(
        '--info_types', action='append',
        help='Strings representing info types to look for. A full list of '
             'info categories and types is available from the API. Examples '
             'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
             'If unspecified, the three above examples will be used.',
        default=['FIRST_NAME', 'LAST_NAME', 'EMAIL_ADDRESS'])
    mask_parser.add_argument(
        'project',
        help='The Google Cloud project id to use as a parent resource.')
    mask_parser.add_argument('item', help='The string to deidentify.')
    mask_parser.add_argument(
        '-n', '--number_to_mask',
        type=int,
        default=0,
        help='The maximum number of sensitive characters to mask in a match. '
        'If omitted the request or set to 0, the API will mask any mathcing '
        'characters.')
    mask_parser.add_argument(
        '-m', '--masking_character',
        help='The character to mask matching sensitive data with.')

    fpe_parser = subparsers.add_parser(
        'deid_fpe',
        help='Deidentify sensitive data in a string using Format Preserving '
             'Encryption (FPE).')
    fpe_parser.add_argument(
        '--info_types', action='append',
        help='Strings representing info types to look for. A full list of '
             'info categories and types is available from the API. Examples '
             'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
             'If unspecified, the three above examples will be used.',
        default=['FIRST_NAME', 'LAST_NAME', 'EMAIL_ADDRESS'])
    fpe_parser.add_argument(
         'project',
         help='The Google Cloud project id to use as a parent resource.')
    fpe_parser.add_argument(
        'item',
        help='The string to deidentify. '
             'Example: string = \'My SSN is 372819127\'')
    fpe_parser.add_argument(
        'key_name',
        help='The name of the Cloud KMS key used to encrypt (\'wrap\') the '
        'AES-256 key. Example: '
        'key_name = \'projects/YOUR_GCLOUD_PROJECT/locations/YOUR_LOCATION/'
        'keyRings/YOUR_KEYRING_NAME/cryptoKeys/YOUR_KEY_NAME\'')
    fpe_parser.add_argument(
        'wrapped_key',
        help='The encrypted (\'wrapped\') AES-256 key to use. This key should '
        'be encrypted using the Cloud KMS key specified by key_name.')
    fpe_parser.add_argument(
        '-a', '--alphabet', default='ALPHA_NUMERIC',
        help='The set of characters to replace sensitive ones with. Commonly '
        'used subsets of the alphabet include "NUMERIC", "HEXADECIMAL", '
        '"UPPER_CASE_ALPHA_NUMERIC", "ALPHA_NUMERIC", '
        '"FFX_COMMON_NATIVE_ALPHABET_UNSPECIFIED"')
    fpe_parser.add_argument(
        '-s', '--surrogate_type',
        help='The name of the surrogate custom info type to use. Only '
        'necessary if you want to reverse the deidentification process. Can '
        'be essentially any arbitrary string, as long as it doesn\'t appear '
        'in your dataset otherwise.')

    reid_parser = subparsers.add_parser(
        'reid_fpe',
        help='Reidentify sensitive data in a string using Format Preserving '
             'Encryption (FPE).')
    reid_parser.add_argument(
        'project',
        help='The Google Cloud project id to use as a parent resource.')
    reid_parser.add_argument(
        'item',
        help='The string to deidentify. '
             'Example: string = \'My SSN is 372819127\'')
    reid_parser.add_argument(
        'surrogate_type',
        help='The name of the surrogate custom info type to use. Only '
        'necessary if you want to reverse the deidentification process. Can '
        'be essentially any arbitrary string, as long as it doesn\'t appear '
        'in your dataset otherwise.')
    reid_parser.add_argument(
        'key_name',
        help='The name of the Cloud KMS key used to encrypt (\'wrap\') the '
        'AES-256 key. Example: '
        'key_name = \'projects/YOUR_GCLOUD_PROJECT/locations/YOUR_LOCATION/'
        'keyRings/YOUR_KEYRING_NAME/cryptoKeys/YOUR_KEY_NAME\'')
    reid_parser.add_argument(
        'wrapped_key',
        help='The encrypted (\'wrapped\') AES-256 key to use. This key should '
        'be encrypted using the Cloud KMS key specified by key_name.')
    reid_parser.add_argument(
        '-a', '--alphabet', default='ALPHA_NUMERIC',
        help='The set of characters to replace sensitive ones with. Commonly '
        'used subsets of the alphabet include "NUMERIC", "HEXADECIMAL", '
        '"UPPER_CASE_ALPHA_NUMERIC", "ALPHA_NUMERIC", '
        '"FFX_COMMON_NATIVE_ALPHABET_UNSPECIFIED"')

    date_shift_parser = subparsers.add_parser(
        'deid_date_shift',
        help='Deidentify dates in a CSV file by pseudorandomly shifting them.')
    date_shift_parser.add_argument(
        'project',
        help='The Google Cloud project id to use as a parent resource.')
    date_shift_parser.add_argument(
        'input_csv_file',
        help='The path to the CSV file to deidentify. The first row of the '
        'file must specify column names, and all other rows must contain '
        'valid values.')
    date_shift_parser.add_argument(
        'output_csv_file',
        help='The path to save the date-shifted CSV file.')
    date_shift_parser.add_argument(
        'lower_bound_days', type=int,
        help='The maximum number of days to shift a date backward')
    date_shift_parser.add_argument(
        'upper_bound_days', type=int,
        help='The maximum number of days to shift a date forward')
    date_shift_parser.add_argument(
        'date_fields', nargs='+',
        help='The list of date fields in the CSV file to date shift. Example: '
        '[\'birth_date\', \'register_date\']')
    date_shift_parser.add_argument(
        '--context_field_id',
        help='(Optional) The column to determine date shift amount based on. '
        'If this is not specified, a random shift amount will be used for '
        'every row. If this is specified, then \'wrappedKey\' and \'keyName\' '
        'must also be set.')
    date_shift_parser.add_argument(
        '--key_name',
        help='(Optional) The name of the Cloud KMS key used to encrypt '
        '(\'wrap\') the AES-256 key. Example: '
        'key_name = \'projects/YOUR_GCLOUD_PROJECT/locations/YOUR_LOCATION/'
        'keyRings/YOUR_KEYRING_NAME/cryptoKeys/YOUR_KEY_NAME\'')
    date_shift_parser.add_argument(
        '--wrapped_key',
        help='(Optional) The encrypted (\'wrapped\') AES-256 key to use. This '
        'key should be encrypted using the Cloud KMS key specified by'
        'key_name.')

    args = parser.parse_args()

    if args.content == 'deid_mask':
        deidentify_with_mask(args.project, args.item, args.info_types,
                             masking_character=args.masking_character,
                             number_to_mask=args.number_to_mask)
    elif args.content == 'deid_fpe':
        deidentify_with_fpe(args.project, args.item, args.info_types,
                            alphabet=args.alphabet,
                            wrapped_key=args.wrapped_key,
                            key_name=args.key_name,
                            surrogate_type=args.surrogate_type)
    elif args.content == 'reid_fpe':
        reidentify_with_fpe(args.project, args.item,
                            surrogate_type=args.surrogate_type,
                            wrapped_key=args.wrapped_key,
                            key_name=args.key_name, alphabet=args.alphabet)
    elif args.content == 'deid_date_shift':
        deidentify_with_date_shift(args.project,
                                   input_csv_file=args.input_csv_file,
                                   output_csv_file=args.output_csv_file,
                                   lower_bound_days=args.lower_bound_days,
                                   upper_bound_days=args.upper_bound_days,
                                   date_fields=args.date_fields,
                                   context_field_id=args.context_field_id,
                                   wrapped_key=args.wrapped_key,
                                   key_name=args.key_name)
