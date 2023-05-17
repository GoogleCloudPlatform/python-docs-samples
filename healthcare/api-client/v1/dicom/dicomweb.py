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


# [START healthcare_dicomweb_store_instance]
def dicomweb_store_instance(project_id, location, dataset_id, dicom_store_id, dcm_file):
    """Handles the POST requests specified in the DICOMweb standard.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
    before running the sample."""
    # Imports Python's built-in "os" module
    import os

    # Imports the google.auth.transport.requests transport
    from google.auth.transport import requests

    # Imports a module to allow authentication using a service account
    from google.oauth2 import service_account

    # Gets credentials from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    # Creates a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    # URL to the Cloud Healthcare API endpoint and version
    base_url = "https://healthcare.googleapis.com/v1"

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the parent dataset's ID
    # dicom_store_id = 'my-dicom-store' # replace with the DICOM store ID
    # dcm_file = 'dicom000_0001.dcm'  # replace with a DICOM file
    url = f"{base_url}/projects/{project_id}/locations/{location}"

    dicomweb_path = "{}/datasets/{}/dicomStores/{}/dicomWeb/studies".format(
        url, dataset_id, dicom_store_id
    )

    with open(dcm_file, "rb") as dcm:
        dcm_content = dcm.read()

    # Sets required "application/dicom" header on the request
    headers = {"Content-Type": "application/dicom"}

    response = session.post(dicomweb_path, data=dcm_content, headers=headers)
    response.raise_for_status()
    print("Stored DICOM instance:")
    print(response.text)
    return response


# [END healthcare_dicomweb_store_instance]


# [START healthcare_dicomweb_search_instances]
def dicomweb_search_instance(project_id, location, dataset_id, dicom_store_id):
    """Handles the GET requests specified in DICOMweb standard.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
    before running the sample."""
    # Imports Python's built-in "os" module
    import os

    # Imports the google.auth.transport.requests transport
    from google.auth.transport import requests

    # Imports a module to allow authentication using a service account
    from google.oauth2 import service_account

    # Gets credentials from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    # Creates a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    # URL to the Cloud Healthcare API endpoint and version
    base_url = "https://healthcare.googleapis.com/v1"

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the parent dataset's ID
    # dicom_store_id = 'my-dicom-store' # replace with the DICOM store ID
    url = f"{base_url}/projects/{project_id}/locations/{location}"

    dicomweb_path = "{}/datasets/{}/dicomStores/{}/dicomWeb/instances".format(
        url, dataset_id, dicom_store_id
    )

    # Sets required application/dicom+json; charset=utf-8 header on the request
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
    project_id, location, dataset_id, dicom_store_id, study_uid
):
    """Handles the GET requests specified in the DICOMweb standard.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
    before running the sample."""
    # Imports Python's built-in "os" module
    import os

    # Imports the google.auth.transport.requests transport
    from google.auth.transport import requests

    # Imports a module to allow authentication using a service account
    from google.oauth2 import service_account

    # Gets credentials from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    # Creates a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    # URL to the Cloud Healthcare API endpoint and version
    base_url = "https://healthcare.googleapis.com/v1"

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the parent dataset's ID
    # dicom_store_id = 'my-dicom-store' # replace with the DICOM store ID
    # study_uid = '1.3.6.1.4.1.5062.55.1.227'  # replace with the study UID
    url = f"{base_url}/projects/{project_id}/locations/{location}"

    dicomweb_path = "{}/datasets/{}/dicomStores/{}/dicomWeb/studies/{}".format(
        url, dataset_id, dicom_store_id, study_uid
    )

    # When specifying the output file, use an extension like ".multipart."
    # Then, parse the downloaded multipart file to get each individual
    # DICOM file.
    file_name = "study.multipart"

    response = session.get(dicomweb_path)

    response.raise_for_status()

    with open(file_name, "wb") as f:
        f.write(response.content)
        print(f"Retrieved study and saved to {file_name} in current directory")

    return response


# [END healthcare_dicomweb_retrieve_study]


# [START healthcare_dicomweb_search_studies]
def dicomweb_search_studies(project_id, location, dataset_id, dicom_store_id):
    """Handles the GET requests specified in the DICOMweb standard.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
    before running the sample."""
    # Imports Python's built-in "os" module
    import os

    # Imports the google.auth.transport.requests transport
    from google.auth.transport import requests

    # Imports a module to allow authentication using a service account
    from google.oauth2 import service_account

    # Gets credentials from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    # Creates a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    # URL to the Cloud Healthcare API endpoint and version
    base_url = "https://healthcare.googleapis.com/v1"

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the parent dataset's ID
    # dicom_store_id = 'my-dicom-store' # replace with the DICOM store ID
    url = f"{base_url}/projects/{project_id}/locations/{location}"

    dicomweb_path = "{}/datasets/{}/dicomStores/{}/dicomWeb/studies".format(
        url, dataset_id, dicom_store_id
    )

    # Refine your search by appending DICOM tags to the
    # request in the form of query parameters. This sample
    # searches for studies containing a patient's name.
    params = {"PatientName": "Sally Zhang"}

    response = session.get(dicomweb_path, params=params)

    response.raise_for_status()

    print(f"Studies found: response is {response}")

    # Uncomment the following lines to process the response as JSON.
    # patients = response.json()
    # print('Patients found matching query:')
    # print(json.dumps(patients, indent=2))

    # return patients


# [END healthcare_dicomweb_search_studies]


# [START healthcare_dicomweb_retrieve_instance]
def dicomweb_retrieve_instance(
    project_id,
    location,
    dataset_id,
    dicom_store_id,
    study_uid,
    series_uid,
    instance_uid,
):
    """Handles the GET requests specified in the DICOMweb standard.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
    before running the sample."""
    # Imports Python's built-in "os" module
    import os

    # Imports the google.auth.transport.requests transport
    from google.auth.transport import requests

    # Imports a module to allow authentication using a service account
    from google.oauth2 import service_account

    # Gets credentials from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    # Creates a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    # URL to the Cloud Healthcare API endpoint and version
    base_url = "https://healthcare.googleapis.com/v1"

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the parent dataset's ID
    # dicom_store_id = 'my-dicom-store' # replace with the DICOM store ID
    # study_uid = '1.3.6.1.4.1.5062.55.1.2270943358.716200484.1363785608958.61.0'  # replace with the study UID
    # series_uid = '2.24.52329571877967561426579904912379710633'  # replace with the series UID
    # instance_uid = '1.3.6.2.4.2.14619.5.2.1.6280.6001.129311971280445372188125744148'  # replace with the instance UID
    url = f"{base_url}/projects/{project_id}/locations/{location}"

    dicom_store_path = "{}/datasets/{}/dicomStores/{}".format(
        url, dataset_id, dicom_store_id
    )

    dicomweb_path = "{}/dicomWeb/studies/{}/series/{}/instances/{}".format(
        dicom_store_path, study_uid, series_uid, instance_uid
    )

    file_name = "instance.dcm"

    # Set the required Accept header on the request
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
    project_id,
    location,
    dataset_id,
    dicom_store_id,
    study_uid,
    series_uid,
    instance_uid,
):
    """Handles the GET requests specified in the DICOMweb standard.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
    before running the sample."""
    # Imports Python's built-in "os" module
    import os

    # Imports the google.auth.transport.requests transport
    from google.auth.transport import requests

    # Imports a module to allow authentication using a service account
    from google.oauth2 import service_account

    # Gets credentials from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    # Creates a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    # URL to the Cloud Healthcare API endpoint and version
    base_url = "https://healthcare.googleapis.com/v1"

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the parent dataset's ID
    # dicom_store_id = 'my-dicom-store' # replace with the DICOM store ID
    # study_uid = '1.3.6.1.4.1.5062.55.1.2270943358.716200484.1363785608958.61.0'  # replace with the study UID
    # series_uid = '2.24.52329571877967561426579904912379710633'  # replace with the series UID
    # instance_uid = '1.3.6.2.4.2.14619.5.2.1.6280.6001.129311971280445372188125744148'  # replace with the instance UID
    url = f"{base_url}/projects/{project_id}/locations/{location}"

    dicom_store_path = "{}/datasets/{}/dicomStores/{}".format(
        url, dataset_id, dicom_store_id
    )

    dicomweb_path = "{}/dicomWeb/studies/{}/series/{}/instances/{}/rendered".format(
        dicom_store_path, study_uid, series_uid, instance_uid
    )

    file_name = "rendered_image.png"

    # Sets the required Accept header on the request for a PNG image
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
def dicomweb_delete_study(project_id, location, dataset_id, dicom_store_id, study_uid):
    """Handles DELETE requests equivalent to the GET requests specified in
    the WADO-RS standard.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
    before running the sample."""
    # Imports Python's built-in "os" module
    import os

    # Imports the google.auth.transport.requests transport
    from google.auth.transport import requests

    # Imports a module to allow authentication using a service account
    from google.oauth2 import service_account

    # Gets credentials from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    # Creates a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    # URL to the Cloud Healthcare API endpoint and version
    base_url = "https://healthcare.googleapis.com/v1"

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the parent dataset's ID
    # dicom_store_id = 'my-dicom-store' # replace with the DICOM store ID
    # study_uid = '1.3.6.1.4.1.5062.55.1.2270943358.716200484.1363785608958.61.0'  # replace with the study UID
    url = f"{base_url}/projects/{project_id}/locations/{location}"

    dicomweb_path = "{}/datasets/{}/dicomStores/{}/dicomWeb/studies/{}".format(
        url, dataset_id, dicom_store_id, study_uid
    )

    # Sets the required application/dicom+json; charset=utf-8 header on the request
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

    parser.add_argument(
        "--project_id",
        default=(os.environ.get("GOOGLE_CLOUD_PROJECT")),
        help="GCP project name",
    )

    parser.add_argument("--location", default="us-central1", help="GCP location")

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
            args.project_id,
            args.location,
            args.dataset_id,
            args.dicom_store_id,
            args.dcm_file,
        )

    elif args.command == "dicomweb-search-instance":
        dicomweb_search_instance(
            args.project_id,
            args.location,
            args.dataset_id,
            args.dicom_store_id,
        )

    elif args.command == "dicomweb-retrieve-study":
        dicomweb_retrieve_study(
            args.project_id,
            args.location,
            args.dataset_id,
            args.dicom_store_id,
            args.study_uid,
        )

    elif args.command == "dicomweb-retrieve-instance":
        dicomweb_retrieve_instance(
            args.project_id,
            args.location,
            args.dataset_id,
            args.dicom_store_id,
            args.study_uid,
            args.series_uid,
            args.instance_uid,
        )

    elif args.command == "dicomweb-search-studies":
        dicomweb_search_studies(
            args.project_id,
            args.location,
            args.dataset_id,
            args.dicom_store_id,
        )

    elif args.command == "dicomweb-retrieve-rendered":
        dicomweb_retrieve_rendered(
            args.project_id,
            args.location,
            args.dataset_id,
            args.dicom_store_id,
            args.study_uid,
            args.series_uid,
            args.instance_uid,
        )

    elif args.command == "dicomweb-delete-study":
        dicomweb_delete_study(
            args.project_id,
            args.location,
            args.dataset_id,
            args.dicom_store_id,
            args.study_uid,
        )


def main():
    args = parse_command_line_args()
    run_command(args)


if __name__ == "__main__":
    main()
