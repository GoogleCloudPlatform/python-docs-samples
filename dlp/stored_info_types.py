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

"""Sample app that sets up Data Loss Prevention API stored infoTypes."""

from __future__ import print_function

import argparse
import os
import time


# [START dlp_create_stored_info_type]
def create_stored_info_type_from_gcs_files(
            project, gcs_input_file_path,
            gcs_output_path, stored_info_type_id=None,
            display_name=None, description=None):
    """Creates a scheduled Data Loss Prevention API stored infoType from a set
        of GCS files.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        gcs_input_file_path: The path specifying the input files containing the
            dictionary words.
        gcs_output_path: The path specifying where the dictionary data files
            should be stored.
        stored_info_type_id: The id of the stored infoType. If omitted, an id
            will be randomly generated.
        display_name: The optional display name of the stored infoType.
        description: The optional description of the stored infoType.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Prepare the dictionary config.
    dictionary_config = {
        'output_path': {'path': gcs_output_path},
        'cloud_storage_file_set': {'url': gcs_input_file_path},
    }
    create_stored_info_type(
        project, dictionary_config, stored_info_type_id=stored_info_type_id,
        display_name=display_name, description=description)


def create_stored_info_type_from_bq_table(
            project, bq_input_project_id, bq_input_dataset_id,
            bq_input_table_id, bq_input_table_field, gcs_output_path,
            stored_info_type_id=None, display_name=None, description=None):
    """Creates a scheduled Data Loss Prevention API stored infoType from a
        column of a BigQuery.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        bq_input_project_id: The id of the project owning the input BigQuery
            table.
        bq_input_dataset_id: The dataset of the input BigQuery table.
        bq_input_table_id: The id of the input BigQuery table.
        bq_input_table_field: The name of the field of the BigQuery table_id
            containing the dictionary words.
        gcs_output_path: The path specifying where the dictionary data files
            should be stored.
        stored_info_type_id: The id of the stored infoType. If omitted, an id
            will be randomly generated.
        display_name: The optional display name of the stored infoType.
        description: The optional description of the stored infoType.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Prepare the dictionary config.
    dictionary_config = {
        'output_path': {'path': gcs_output_path},
        'big_query_field': {
            'table': {
                'project_id': bq_input_project_id,
                'dataset_id': bq_input_dataset_id,
                'table_id': bq_input_table_id,
            },
            'field': {'name': bq_input_table_field},
        }
    }
    create_stored_info_type(project, dictionary_config,
                            stored_info_type_id=stored_info_type_id,
                            display_name=display_name, description=description)


def create_stored_info_type(project, dictionary_config,
                            stored_info_type_id=None, display_name=None,
                            description=None):
    """Creates a scheduled Data Loss Prevention API stored infoType from a
        column of a BigQuery.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        dictionary_config: The config for the large custom dictionary.
        stored_info_type_id: The id of the stored infoType. If omitted, an id
            will be randomly generated.
        display_name: The optional display name of the stored infoType.
        description: The optional description of the stored infoType.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Import the client library
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp.DlpServiceClient()

    # Create the stored infoType config.
    stored_info_type_config = {
        'display_name': display_name,
        'description': description,
        'large_custom_dictionary': dictionary_config
    }

    # Convert the project id into a full resource id.
    parent = dlp.project_path(project)

    # Call the API.
    response = dlp.create_stored_info_type(
        parent, config=stored_info_type_config,
        stored_info_type_id=stored_info_type_id)

    print('Successfully created stored infoType {}'.format(response.name))

# [END dlp_create_stored_info_type]


# [START dlp_list_stored_info_types]
def list_stored_info_types(project):
    """Lists all Data Loss Prevention API stored infoTypes.
    Args:
        project: The Google Cloud project id to use as a parent resource.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Import the client library
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = dlp.project_path(project)

    # Call the API.
    response = dlp.list_stored_info_types(parent)

    # Define a helper function to convert the API's "seconds since the epoch"
    # time format into a human-readable string.
    def human_readable_time(timestamp):
        return str(time.localtime(timestamp.seconds))

    for stored_info_type in response:
        print('Stored infoType {}:'.format(stored_info_type.name))
        if stored_info_type.current_version:
            version = stored_info_type.current_version
            print('  Current version:')
            print('    Created: {}'.format(
                human_readable_time(version.create_time)))
            print('    State: {}'.format(version.state))
            print('    Error count: {}'.format(len(version.errors)))
        if stored_info_type.pending_versions:
            print('  Pending versions:')
            for version in stored_info_type.pending_versions:
                print('    Created: {}'.format(
                    human_readable_time(version.create_time)))
                print('    State: {}'.format(version.state))
                print('    Error count: {}'.format(len(version.errors)))

# [END dlp_list_stored_info_types]


# [START dlp_delete_stored_info_type]
def delete_stored_info_type(project, stored_info_type_id):
    """Deletes a Data Loss Prevention API stored infoType.
    Args:
        project: The id of the Google Cloud project which owns the stored
            infoType.
        stored_info_type_id: The id of the stored infoType to delete.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Import the client library
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = dlp.project_path(project)

    # Combine the stored infoType id with the parent id.
    stored_info_type_resource = '{}/storedInfoTypes/{}'.format(
        parent, stored_info_type_id)

    # Call the API.
    dlp.delete_stored_info_type(stored_info_type_resource)

    print('Stored infoType {} successfully deleted.'.format(
        stored_info_type_resource))

# [END dlp_delete_stored_info_type]


if __name__ == '__main__':
    default_project = os.environ.get('GCLOUD_PROJECT')

    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(
        dest='action', help='Select which action to perform.')
    subparsers.required = True

    parser_create = subparsers.add_parser(
        'create',
        help='Create a stored infoType.')
    parser_create.add_argument(
        '--gcs_input_file_path',
        help='GCS path of the input files containing the dictionary words.')
    parser_create.add_argument(
        '--bq_input_project_id',
        help='Project of the BigQuery table containing the dictionary words.',
        default=default_project)
    parser_create.add_argument(
        '--bq_input_dataset_id',
        help='Dataset of the BigQuery table containing the dictionary words.')
    parser_create.add_argument(
        '--bq_input_table_id',
        help='ID of the BigQuery table containing the dictionary words.')
    parser_create.add_argument(
        '--bq_input_table_field',
        help='Field of the BigQuery table containing the dictionary words.')
    parser_create.add_argument(
        '--gcs_output_path',
        help='GCS path where the output data files should be stored.')
    parser_create.add_argument(
        '--stored_info_type_id',
        help='The id of the stored infoType. If omitted, an id will be '
             'randomly generated')
    parser_create.add_argument(
        '--display_name',
        help='The optional display name of the stored infoType.')
    parser_create.add_argument(
        '--description',
        help='The optional description of the stored infoType.')
    parser_create.add_argument(
        '--project',
        help='The Google Cloud project id to use as a parent resource.',
        default=default_project)

    parser_list = subparsers.add_parser(
        'list',
        help='List all stored infoTypes.')
    parser_list.add_argument(
        '--project',
        help='The Google Cloud project id to use as a parent resource.',
        default=default_project)

    parser_delete = subparsers.add_parser(
        'delete',
        help='Delete a stored infoType.')
    parser_delete.add_argument(
        'stored_info_type_id',
        help='The id of the stored infoType to delete.')
    parser_delete.add_argument(
        '--project',
        help='The Google Cloud project id to use as a parent resource.',
        default=default_project)

    args = parser.parse_args()

    if args.action == 'create':
        if args.gcs_input_file_path:
            create_stored_info_type_from_gcs_files(
                args.project, args.gcs_input_file_path, args.gcs_output_path,
                stored_info_type_id=args.stored_info_type_id,
                display_name=args.display_name, description=args.description
            )
        else:
            create_stored_info_type_from_bq_table(
                args.project, args.bq_input_project_id,
                args.bq_input_dataset_id, args.bq_input_table_id,
                args.bq_input_table_field, args.gcs_output_path,
                stored_info_type_id=args.stored_info_type_id,
                display_name=args.display_name, description=args.description
            )
    elif args.action == 'list':
        list_stored_info_types(args.project)
    elif args.action == 'delete':
        delete_stored_info_type(args.project, args.stored_info_type_id)
