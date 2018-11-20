# Copyright 2018 Google LLC All Rights Reserved.
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

import argparse
import json
import os

import email
from email import encoders
from email.mime import application
from email.mime import multipart

from google.auth.transport import requests
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

_BASE_URL = 'https://healthcare.googleapis.com/v1alpha'


def get_session(service_account_json):
    """Returns an authorized Requests Session class using the service account
    credentials JSON. This class is used to perform requests to the
    Cloud Healthcare API endpoint."""

    # Pass in the credentials and project ID. If none supplied, get them
    # from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        service_account_json)
    scoped_credentials = credentials.with_scopes(
        ['https://www.googleapis.com/auth/cloud-platform'])

    # Create a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    return session


# [START healthcare_dicomweb_store_instance]
def dicomweb_store_instance(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id,
        dcm_file):
    """Handles the POST requests specified in the DICOMweb standard."""
    url = '{}/projects/{}/locations/{}'.format(base_url,
                                               project_id, cloud_region)

    dicomweb_path = '{}/datasets/{}/dicomStores/{}/dicomWeb/studies'.format(
        url, dataset_id, dicom_store_id)

    # Make an authenticated API request
    session = get_session(service_account_json)

    with open(dcm_file) as dcm:
        dcm_content = dcm.read()

    # All requests to store an instance are multipart messages, as designated
    # by the multipart/related portion of the Content-Type. This means that
    # the request is made up of multiple sets of data that are combined after
    # the request completes. Each of these sets of data must be separated using
    # a boundary, as designated by the boundary portion of the Content-Type.
    multipart_body = multipart.MIMEMultipart(
        subtype='related', boundary=email.generator._make_boundary())
    part = application.MIMEApplication(
        dcm_content, 'dicom', _encoder=encoders.encode_noop)
    multipart_body.attach(part)
    boundary = multipart_body.get_boundary()

    content_type = (
        'multipart/related; type="application/dicom"; ' +
        'boundary="%s"') % boundary
    headers = {'Content-Type': content_type}

    try:
        response = session.post(
            dicomweb_path,
            data=multipart_body.as_string(),
            headers=headers)
        response.raise_for_status()
        print('Stored DICOM instance:')
        print(response.text)
        return response
    except HttpError as err:
        print(err)
        return ""
# [END healthcare_dicomweb_store_instance]


# [START healthcare_dicomweb_search_instance]
def dicomweb_search_instance(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id):
    """Handles the GET requests specified in DICOMweb standard."""
    url = '{}/projects/{}/locations/{}'.format(base_url,
                                               project_id, cloud_region)

    dicomweb_path = '{}/datasets/{}/dicomStores/{}/dicomWeb/instances'.format(
        url, dataset_id, dicom_store_id)

    # Make an authenticated API request
    session = get_session(service_account_json)

    headers = {
        'Content-Type': 'application/dicom+json; charset=utf-8'
    }

    response = session.get(dicomweb_path, headers=headers)
    response.raise_for_status()

    instances = response.json()

    print('Instances:')
    print(json.dumps(instances, indent=2))

    return instances
# [END healthcare_dicomweb_search_instance]


# [START healthcare_dicomweb_retrieve_study]
def dicomweb_retrieve_study(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id,
        study_uid):
    """Handles the GET requests specified in the DICOMweb standard."""
    url = '{}/projects/{}/locations/{}'.format(base_url,
                                               project_id, cloud_region)

    dicomweb_path = '{}/datasets/{}/dicomStores/{}/dicomWeb/studies/{}'.format(
        url, dataset_id, dicom_store_id, study_uid)

    # Make an authenticated API request
    session = get_session(service_account_json)

    headers = {
        'Content-Type': 'application/dicom+json; charset=utf-8'
    }

    response = session.get(dicomweb_path, headers=headers)
    response.raise_for_status()

    print('Retrieved study with UID: {}'.format(study_uid))

    return response
# [END healthcare_dicomweb_retrieve_study]


# [START healthcare_dicomweb_delete_study]
def dicomweb_delete_study(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id,
        study_uid):
    """Handles DELETE requests equivalent to the GET requests specified in
    the WADO-RS standard.
    """
    url = '{}/projects/{}/locations/{}'.format(base_url,
                                               project_id, cloud_region)

    dicomweb_path = '{}/datasets/{}/dicomStores/{}/dicomWeb/studies/{}'.format(
        url, dataset_id, dicom_store_id, study_uid)

    # Make an authenticated API request
    session = get_session(service_account_json)

    headers = {
        'Content-Type': 'application/dicom+json; charset=utf-8'
    }

    response = session.delete(dicomweb_path, headers=headers)
    response.raise_for_status()

    print('Deleted study.')

    return response
# [END healthcare_dicomweb_delete_study]


def parse_command_line_args():
    """Parses command line arguments."""

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '--service_account_json',
        default=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
        help='Path to service account JSON file.')

    parser.add_argument(
        '--base_url',
        default=_BASE_URL,
        help='Healthcare API URL')

    parser.add_argument(
        '--project_id',
        default=(os.environ.get("GOOGLE_CLOUD_PROJECT")),
        help='GCP project name')

    parser.add_argument(
        '--cloud_region',
        default='us-central1',
        help='GCP region')

    parser.add_argument(
        '--dataset_id',
        default=None,
        help='Name of dataset')

    parser.add_argument(
        '--dicom_store_id',
        default=None,
        help='Name of DICOM store')

    parser.add_argument(
        '--dcm_file',
        default=None,
        help='File name for DCM file to store.')

    parser.add_argument(
        '--study_uid',
        default=None,
        help='Unique identifier for a study.')

    command = parser.add_subparsers(dest='command')

    command.add_parser(
        'dicomweb-store-instance',
        help=dicomweb_store_instance.__doc__)
    command.add_parser(
        'dicomweb-search-instance',
        help=dicomweb_search_instance.__doc__)
    command.add_parser(
        'dicomweb-retrieve-study',
        help=dicomweb_retrieve_study.__doc__)
    command.add_parser(
        'dicomweb-delete-study',
        help=dicomweb_delete_study.__doc__)

    return parser.parse_args()


def run_command(args):
    """Calls the program using the specified command."""
    if args.project_id is None:
        print('You must specify a project ID or set the '
              '"GOOGLE_CLOUD_PROJECT" environment variable.')
        return

    elif args.command == 'dicomweb-store-instance':
        dicomweb_store_instance(
            args.service_account_json,
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.dicom_store_id,
            args.dcm_file)

    elif args.command == 'dicomweb-search-instance':
        dicomweb_search_instance(
            args.service_account_json,
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.dicom_store_id)

    elif args.command == 'dicomweb-retrieve-study':
        dicomweb_retrieve_study(
            args.service_account_json,
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.dicom_store_id,
            args.study_uid)

    elif args.command == 'dicomweb-delete-study':
        dicomweb_delete_study(
            args.service_account_json,
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.dicom_store_id,
            args.study_uid)


def main():
    args = parse_command_line_args()
    run_command(args)


if __name__ == '__main__':
    main()
