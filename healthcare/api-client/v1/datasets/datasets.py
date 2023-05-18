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
import os


# [START healthcare_create_dataset]
def create_dataset(project_id, location, dataset_id):
    """Creates a dataset.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/datasets
    before running the sample."""
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"
    # Instantiates an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the dataset's location
    # dataset_id = 'my-dataset'  # replace with your dataset ID
    dataset_parent = f"projects/{project_id}/locations/{location}"

    request = (
        client.projects()
        .locations()
        .datasets()
        .create(parent=dataset_parent, body={}, datasetId=dataset_id)
    )

    response = request.execute()
    print(f"Created dataset: {dataset_id}")
    return response


# [END healthcare_create_dataset]


# [START healthcare_delete_dataset]
def delete_dataset(project_id, location, dataset_id):
    """Deletes a dataset.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/datasets
    before running the sample."""
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"
    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the dataset's location
    # dataset_id = 'my-dataset'  # replace with your dataset ID
    dataset_name = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )

    request = client.projects().locations().datasets().delete(name=dataset_name)

    response = request.execute()
    print(f"Deleted dataset: {dataset_id}")
    return response


# [END healthcare_delete_dataset]


# [START healthcare_get_dataset]
def get_dataset(project_id, location, dataset_id):
    """Gets any metadata associated with a dataset.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/datasets
    before running the sample."""
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"
    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the dataset's location
    # dataset_id = 'my-dataset'  # replace with your dataset ID
    dataset_name = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )

    datasets = client.projects().locations().datasets()
    dataset = datasets.get(name=dataset_name).execute()

    print("Name: {}".format(dataset.get("name")))
    print("Time zone: {}".format(dataset.get("timeZone")))

    return dataset


# [END healthcare_get_dataset]


# [START healthcare_list_datasets]
def list_datasets(project_id, location):
    """Lists the datasets in the project.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/datasets
    before running the sample."""
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"
    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the location of the datasets
    dataset_parent = f"projects/{project_id}/locations/{location}"

    datasets = (
        client.projects()
        .locations()
        .datasets()
        .list(parent=dataset_parent)
        .execute()
        .get("datasets", [])
    )

    for dataset in datasets:
        print(
            "Dataset: {}\nTime zone: {}".format(
                dataset.get("name"), dataset.get("timeZone")
            )
        )

    return datasets


# [END healthcare_list_datasets]


# [START healthcare_patch_dataset]
def patch_dataset(project_id, location, dataset_id, time_zone):
    """Updates dataset metadata.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/datasets
    before running the sample."""
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"
    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the dataset's location
    # dataset_id = 'my-dataset'  # replace with your dataset ID
    # time_zone = 'GMT'  # replace with the dataset's time zone
    dataset_parent = f"projects/{project_id}/locations/{location}"
    dataset_name = f"{dataset_parent}/datasets/{dataset_id}"

    # Sets the time zone
    patch = {"timeZone": time_zone}

    request = (
        client.projects()
        .locations()
        .datasets()
        .patch(name=dataset_name, updateMask="timeZone", body=patch)
    )

    response = request.execute()
    print(f"Patched dataset {dataset_id} with time zone: {time_zone}")
    return response


# [END healthcare_patch_dataset]


# [START healthcare_dicom_keeplist_deidentify_dataset]
def deidentify_dataset(project_id, location, dataset_id, destination_dataset_id):
    """Uses a DICOM tag keeplist to create a new dataset containing
    de-identified DICOM data from the source dataset.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/datasets
    before running the sample."""
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"
    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the dataset's location
    # dataset_id = 'my-source-dataset'  # replace with the source dataset's ID
    # destination_dataset_id = 'my-destination-dataset'  # replace with the destination dataset's ID
    source_dataset = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    destination_dataset = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, destination_dataset_id
    )

    body = {
        "destinationDataset": destination_dataset,
        "config": {
            "dicom": {
                "keepList": {
                    "tags": [
                        "Columns",
                        "NumberOfFrames",
                        "PixelRepresentation",
                        "MediaStorageSOPClassUID",
                        "MediaStorageSOPInstanceUID",
                        "Rows",
                        "SamplesPerPixel",
                        "BitsAllocated",
                        "HighBit",
                        "PhotometricInterpretation",
                        "BitsStored",
                        "PatientID",
                        "TransferSyntaxUID",
                        "SOPInstanceUID",
                        "StudyInstanceUID",
                        "SeriesInstanceUID",
                        "PixelData",
                    ]
                }
            }
        },
    }

    request = (
        client.projects()
        .locations()
        .datasets()
        .deidentify(sourceDataset=source_dataset, body=body)
    )

    response = request.execute()
    print(
        "Data in dataset {} de-identified."
        "De-identified data written to {}".format(dataset_id, destination_dataset_id)
    )
    return response


# [END healthcare_dicom_keeplist_deidentify_dataset]


# [START healthcare_dataset_get_iam_policy]
def get_dataset_iam_policy(project_id, location, dataset_id):
    """Gets the IAM policy for the specified dataset.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/datasets
    before running the sample."""
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"
    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the dataset's location
    # dataset_id = 'my-dataset'  # replace with your dataset ID
    dataset_name = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )

    request = (
        client.projects().locations().datasets().getIamPolicy(resource=dataset_name)
    )
    response = request.execute()

    print("etag: {}".format(response.get("name")))
    return response


# [END healthcare_dataset_get_iam_policy]


# [START healthcare_dataset_set_iam_policy]
def set_dataset_iam_policy(project_id, location, dataset_id, member, role, etag=None):
    """Sets the IAM policy for the specified dataset.

        A single member will be assigned a single role. A member can be any of:

        - allUsers, that is, anyone
        - allAuthenticatedUsers, anyone authenticated with a Google account
        - user:email, as in 'user:somebody@example.com'
        - group:email, as in 'group:admins@example.com'
        - domain:domainname, as in 'domain:example.com'
        - serviceAccount:email,
            as in 'serviceAccount:my-other-app@appspot.gserviceaccount.com'

        A role can be any IAM role, such as 'roles/viewer', 'roles/owner',
        or 'roles/editor'

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/datasets
    before running the sample.
    """
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"
    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the dataset's location
    # dataset_id = 'my-dataset'  # replace with your dataset ID
    dataset_name = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )

    policy = {"bindings": [{"role": role, "members": [member]}]}

    if etag is not None:
        policy["etag"] = etag

    request = (
        client.projects()
        .locations()
        .datasets()
        .setIamPolicy(resource=dataset_name, body={"policy": policy})
    )
    response = request.execute()

    print("etag: {}".format(response.get("name")))
    print("bindings: {}".format(response.get("bindings")))
    return response


# [END healthcare_dataset_set_iam_policy]


def parse_command_line_args():
    """Parses command line arguments."""

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--project_id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        help="GCP project name",
    )

    parser.add_argument("--location", default="us-central1", help="GCP cloud region")

    parser.add_argument("--dataset_id", default=None, help="Name of dataset")

    parser.add_argument(
        "--time_zone", default=None, help="The default timezone used by a dataset"
    )

    parser.add_argument(
        "--destination_dataset_id",
        default=None,
        help="The name of the new dataset where the de-identified data "
        "will be written",
    )

    parser.add_argument(
        "--member",
        default=None,
        help='Member to add to IAM policy (e.g. "domain:example.com")',
    )

    parser.add_argument(
        "--role", default=None, help='IAM Role to give to member (e.g. "roles/viewer")'
    )

    command = parser.add_subparsers(dest="command")

    command.add_parser("create-dataset", help=create_dataset.__doc__)
    command.add_parser("delete-dataset", help=delete_dataset.__doc__)
    command.add_parser("get-dataset", help=get_dataset.__doc__)
    command.add_parser("list-datasets", help=list_datasets.__doc__)
    command.add_parser("patch-dataset", help=patch_dataset.__doc__)
    command.add_parser("get_iam_policy", help=get_dataset_iam_policy.__doc__)
    command.add_parser("set_iam_policy", help=set_dataset_iam_policy.__doc__)

    command.add_parser("deidentify-dataset", help=deidentify_dataset.__doc__)

    return parser.parse_args()


def run_command(args):
    """Calls the program using the specified command."""
    if args.project_id is None:
        print(
            "You must specify a project ID or set the"
            '"GOOGLE_CLOUD_PROJECT" environment variable.'
        )
        return

    elif args.command == "create-dataset":
        create_dataset(args.project_id, args.location, args.dataset_id)

    elif args.command == "delete-dataset":
        delete_dataset(args.project_id, args.location, args.dataset_id)

    elif args.command == "get-dataset":
        get_dataset(args.project_id, args.location, args.dataset_id)

    elif args.command == "list-datasets":
        list_datasets(args.project_id, args.location)

    elif args.command == "patch-dataset":
        patch_dataset(args.project_id, args.location, args.dataset_id, args.time_zone)

    elif args.command == "deidentify-dataset":
        deidentify_dataset(
            args.project_id, args.location, args.dataset_id, args.destination_dataset_id
        )

    elif args.command == "get_iam_policy":
        get_dataset_iam_policy(args.project_id, args.location, args.dataset_id)

    elif args.command == "set_iam_policy":
        set_dataset_iam_policy(
            args.project_id, args.location, args.dataset_id, args.member, args.role
        )


def main():
    args = parse_command_line_args()
    run_command(args)


if __name__ == "__main__":
    main()
