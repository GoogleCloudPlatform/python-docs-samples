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

from google.auth.transport import requests
from google.oauth2 import service_account

_BASE_URL = "https://healthcare.googleapis.com/v1"


def get_session():
    """Creates an authorized Requests Session."""
    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    # Create a requests Session object with the credentials.
    session = requests.AuthorizedSession(credentials)
    return session


# [START healthcare_dicomweb_store_instance]
def dicomweb_store_instance(
    base_url, project_id, cloud_region, dataset_id, dicom_store_id, dcm_file
):
    """Handles the POST requests specified in the DICOMweb standard."""
    url = "{}/projects/{}/locations/{}".format(base_url, project_id, cloud_region)

    dicomweb_path = "{}/datasets/{}/dicomStores/{}/dicomWeb/studies".format(
        url, dataset_id, dicom_store_id
    )

    # Make an authenticated API request
    session = get_session()

    with open(dcm_file, "rb") as dcm:
        dcm_content = dcm.read()

    content_type = "application/dicom"
    headers = {"Content-Type": content_type}

    response = session.post(dicomweb_path, data=dcm_content, headers=headers)
    response.raise_for_status()
    print("Stored DICOM instance:")
    print(response.text)
    return response


# [END healthcare_dicomweb_store_instance]


# [START healthcare_dicomweb_search_instances]
def dicomweb_search_instance(
    base_url, project_id, cloud_region, dataset_id, dicom_store_id
):
    """Handles the GET requests specified in DICOMweb standard."""
    url = "{}/projects/{}/locations/{}".format(base_url, project_id, cloud_region)

    dicomweb_path = "{}/datasets/{}/dicomStores/{}/dicomWeb/instances".format(
        url, dataset_id, dicom_store_id
    )

    # Make an authenticated API request
    session = get_session()

    headers = {"Content-Type": "application/dicom+json; charset=utf-8"}

    response = session.get(dicomweb_path, headers=headers)
    response.raise_for_status()

    instances = response.json()

    print("Instances:")
    print(json.dumps(instances, indent=2))

    return instances


# [END healthcare_dicomweb_search_instances]


# [START healthcare_dicomweb_retrieve_study]
def dicomweb_retrieve_study(
    base_url, project_id, cloud_region, dataset_id, dicom_store_id, study_uid
):
    """Handles the GET requests specified in the DICOMweb standard."""
    url = "{}/projects/{}/locations/{}".format(base_url, project_id, cloud_region)

    dicomweb_path = "{}/datasets/{}/dicomStores/{}/dicomWeb/studies/{}".format(
        url, dataset_id, dicom_store_id, study_uid
    )

    # When specifying the output file, use an extension like ".multipart."
    # Then, parse the downloaded multipart file to get each individual
    # DICOM file.
    file_name = "study.multipart"

    # Make an authenticated API request
    session = get_session()

    response = session.get(dicomweb_path)

    response.raise_for_status()

    with open(file_name, "wb") as f:
        f.write(response.content)
        print("Retrieved study and saved to {} in current directory".format(file_name))

    return response


# [END healthcare_dicomweb_retrieve_study]


# [START healthcare_dicomweb_search_studies]
def dicomweb_search_studies(
    base_url, project_id, cloud_region, dataset_id, dicom_store_id
):
    """Handles the GET requests specified in the DICOMweb standard."""
    url = "{}/projects/{}/locations/{}".format(base_url, project_id, cloud_region)

    dicomweb_path = "{}/datasets/{}/dicomStores/{}/dicomWeb/studies".format(
        url, dataset_id, dicom_store_id
    )

    # Refine your search by appending DICOM tags to the
    # request in the form of query parameters. This sample
    # searches for studies containing a patient's name.
    params = {"PatientName": "Sally Zhang"}

    session = get_session()

    response = session.get(dicomweb_path, params=params)

    response.raise_for_status()

    print("Studies found: response is {}".format(response))

    # Uncomment the following lines to process the response as JSON.
    # patients = response.json()
    # print('Patients found matching query:')
    # print(json.dumps(patients, indent=2))

    # return patients


# [END healthcare_dicomweb_search_studies]


# [START healthcare_dicomweb_retrieve_instance]
def dicomweb_retrieve_instance(
    base_url,
    project_id,
    cloud_region,
    dataset_id,
    dicom_store_id,
    study_uid,
    series_uid,
    instance_uid,
):
    """Handles the GET requests specified in the DICOMweb standard."""
    url = "{}/projects/{}/locations/{}".format(base_url, project_id, cloud_region)

    dicom_store_path = "{}/datasets/{}/dicomStores/{}".format(
        url, dataset_id, dicom_store_id
    )

    dicomweb_path = "{}/dicomWeb/studies/{}/series/{}/instances/{}".format(
        dicom_store_path, study_uid, series_uid, instance_uid
    )

    file_name = "instance.dcm"

    # Make an authenticated API request
    session = get_session()

    headers = {"Accept": "application/dicom; transfer-syntax=*"}
    response = session.get(dicomweb_path, headers=headers)
    response.raise_for_status()

    with open(file_name, "wb") as f:
        f.write(response.content)
        print(
            "Retrieved DICOM instance and saved to {} in current directory".format(
                file_name
            )
        )

    return response


# [END healthcare_dicomweb_retrieve_instance]


# [START healthcare_dicomweb_retrieve_rendered]
def dicomweb_retrieve_rendered(
    base_url,
    project_id,
    cloud_region,
    dataset_id,
    dicom_store_id,
    study_uid,
    series_uid,
    instance_uid,
):
    """Handles the GET requests specified in the DICOMweb standard."""
    url = "{}/projects/{}/locations/{}".format(base_url, project_id, cloud_region)

    dicom_store_path = "{}/datasets/{}/dicomStores/{}".format(
        url, dataset_id, dicom_store_id
    )

    instance_path = "{}/dicomWeb/studies/{}/series/{}/instances/{}".format(
        dicom_store_path, study_uid, series_uid, instance_uid
    )

    dicomweb_path = "{}/rendered".format(instance_path)

    file_name = "rendered_image.png"

    # Make an authenticated API request
    session = get_session()

    headers = {"Accept": "image/png"}
    response = session.get(dicomweb_path, headers=headers)
    response.raise_for_status()

    with open(file_name, "wb") as f:
        f.write(response.content)
        print(
            "Retrieved rendered image and saved to {} in current directory".format(
                file_name
            )
        )

    return response


# [END healthcare_dicomweb_retrieve_rendered]


# [START healthcare_dicomweb_delete_study]
def dicomweb_delete_study(
    base_url, project_id, cloud_region, dataset_id, dicom_store_id, study_uid
):
    """Handles DELETE requests equivalent to the GET requests specified in
    the WADO-RS standard.
    """
    url = "{}/projects/{}/locations/{}".format(base_url, project_id, cloud_region)

    dicomweb_path = "{}/datasets/{}/dicomStores/{}/dicomWeb/studies/{}".format(
        url, dataset_id, dicom_store_id, study_uid
    )

    # Make an authenticated API request
    session = get_session()

    headers = {"Content-Type": "application/dicom+json; charset=utf-8"}

    response = session.delete(dicomweb_path, headers=headers)
    response.raise_for_status()

    print("Deleted study.")

    return response


# [END healthcare_dicomweb_delete_study]


def parse_command_line_args():
    """Parses command line arguments."""

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--base_url", default=_BASE_URL, help="Healthcare API URL")

    parser.add_argument(
        "--project_id",
        default=(os.environ.get("GOOGLE_CLOUD_PROJECT")),
        help="GCP project name",
    )

    parser.add_argument("--cloud_region", default="us-central1", help="GCP region")

    parser.add_argument("--dataset_id", default=None, help="Name of dataset")

    parser.add_argument("--dicom_store_id", default=None, help="Name of DICOM store")

    parser.add_argument(
        "--dcm_file", default=None, help="File name for DCM file to store."
    )

    parser.add_argument(
        "--study_uid", default=None, help="Unique identifier for a study."
    )

    parser.add_argument(
        "--series_uid", default=None, help="Unique identifier for a series."
    )

    parser.add_argument(
        "--instance_uid", default=None, help="Unique identifier for an instance."
    )

    command = parser.add_subparsers(dest="command")

    command.add_parser("dicomweb-store-instance", help=dicomweb_store_instance.__doc__)
    command.add_parser(
        "dicomweb-search-instance", help=dicomweb_search_instance.__doc__
    )
    command.add_parser("dicomweb-retrieve-study", help=dicomweb_retrieve_study.__doc__)
    command.add_parser("dicomweb-search-studies", help=dicomweb_search_studies.__doc__)
    command.add_parser(
        "dicomweb-retrieve-instance", help=dicomweb_retrieve_instance.__doc__
    )
    command.add_parser(
        "dicomweb-retrieve-rendered", help=dicomweb_retrieve_rendered.__doc__
    )
    command.add_parser("dicomweb-delete-study", help=dicomweb_delete_study.__doc__)

    return parser.parse_args()


def run_command(args):
    """Calls the program using the specified command."""
    if args.project_id is None:
        print(
            "You must specify a project ID or set the "
            '"GOOGLE_CLOUD_PROJECT" environment variable.'
        )
        return

    elif args.command == "dicomweb-store-instance":
        dicomweb_store_instance(
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.dicom_store_id,
            args.dcm_file,
        )

    elif args.command == "dicomweb-search-instance":
        dicomweb_search_instance(
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.dicom_store_id,
        )

    elif args.command == "dicomweb-retrieve-study":
        dicomweb_retrieve_study(
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.dicom_store_id,
            args.study_uid,
        )

    elif args.command == "dicomweb-retrieve-instance":
        dicomweb_retrieve_instance(
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.dicom_store_id,
            args.study_uid,
            args.series_uid,
            args.instance_uid,
        )

    elif args.command == "dicomweb-search-studies":
        dicomweb_search_studies(
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.dicom_store_id,
        )

    elif args.command == "dicomweb-retrieve-rendered":
        dicomweb_retrieve_rendered(
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.dicom_store_id,
            args.study_uid,
            args.series_uid,
            args.instance_uid,
        )

    elif args.command == "dicomweb-delete-study":
        dicomweb_delete_study(
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.dicom_store_id,
            args.study_uid,
        )


def main():
    args = parse_command_line_args()
    run_command(args)


if __name__ == "__main__":
    main()
