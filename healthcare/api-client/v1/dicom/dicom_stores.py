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


# [START healthcare_create_dicom_store]
def create_dicom_store(project_id, location, dataset_id, dicom_store_id):
    """Creates a new DICOM store within the parent dataset.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
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
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the DICOM store's parent dataset ID
    # dicom_store_id = 'my-dicom-store'  # replace with the DICOM store's ID
    dicom_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )

    request = (
        client.projects()
        .locations()
        .datasets()
        .dicomStores()
        .create(parent=dicom_store_parent, body={}, dicomStoreId=dicom_store_id)
    )

    response = request.execute()
    print(f"Created DICOM store: {dicom_store_id}")
    return response


# [END healthcare_create_dicom_store]


# [START healthcare_delete_dicom_store]
def delete_dicom_store(project_id, location, dataset_id, dicom_store_id):
    """Deletes the specified DICOM store.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
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
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the DICOM store's parent dataset ID
    # dicom_store_id = 'my-dicom-store'  # replace with the DICOM store's ID
    dicom_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    dicom_store_name = f"{dicom_store_parent}/dicomStores/{dicom_store_id}"

    request = (
        client.projects()
        .locations()
        .datasets()
        .dicomStores()
        .delete(name=dicom_store_name)
    )

    response = request.execute()
    print(f"Deleted DICOM store: {dicom_store_id}")
    return response


# [END healthcare_delete_dicom_store]


# [START healthcare_get_dicom_store]
def get_dicom_store(project_id, location, dataset_id, dicom_store_id):
    """Gets the specified DICOM store.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
    before running the sample."""
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    # Imports Python's built-in "json" module
    import json

    api_version = "v1"
    service_name = "healthcare"
    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the DICOM store's parent dataset ID
    # dicom_store_id = 'my-dicom-store'  # replace with the DICOM store's ID
    dicom_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    dicom_store_name = f"{dicom_store_parent}/dicomStores/{dicom_store_id}"

    dicom_stores = client.projects().locations().datasets().dicomStores()
    dicom_store = dicom_stores.get(name=dicom_store_name).execute()

    print(json.dumps(dicom_store, indent=2))
    return dicom_store


# [END healthcare_get_dicom_store]


# [START healthcare_list_dicom_stores]
def list_dicom_stores(project_id, location, dataset_id):
    """Lists the DICOM stores in the given dataset.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
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
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the DICOM store's parent dataset ID
    dicom_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )

    dicom_stores = (
        client.projects()
        .locations()
        .datasets()
        .dicomStores()
        .list(parent=dicom_store_parent)
        .execute()
        .get("dicomStores", [])
    )

    for dicom_store in dicom_stores:
        print(dicom_store)

    return dicom_stores


# [END healthcare_list_dicom_stores]


# [START healthcare_patch_dicom_store]
def patch_dicom_store(project_id, location, dataset_id, dicom_store_id, pubsub_topic):
    """Updates the DICOM store.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
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
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the DICOM store's parent dataset ID
    # dicom_store_id = 'my-dicom-store'  # replace with the DICOM store's ID
    # pubsub_topic = 'my-topic'  # replace with an existing Pub/Sub topic
    dicom_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    dicom_store_name = f"{dicom_store_parent}/dicomStores/{dicom_store_id}"

    patch = {
        "notificationConfig": {
            "pubsubTopic": f"projects/{project_id}/topics/{pubsub_topic}"
        }
    }

    request = (
        client.projects()
        .locations()
        .datasets()
        .dicomStores()
        .patch(name=dicom_store_name, updateMask="notificationConfig", body=patch)
    )

    response = request.execute()
    print(
        "Patched DICOM store {} with Cloud Pub/Sub topic: {}".format(
            dicom_store_id, pubsub_topic
        )
    )

    return response


# [END healthcare_patch_dicom_store]


# [START healthcare_export_dicom_instance_gcs]
def export_dicom_instance(project_id, location, dataset_id, dicom_store_id, uri_prefix):
    """Export data to a Google Cloud Storage bucket by copying
    it from the DICOM store.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
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
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the DICOM store's parent dataset ID
    # dicom_store_id = 'my-dicom-store'  # replace with the DICOM store's ID
    # uri_prefix = 'my-bucket'  # replace with a Cloud Storage bucket
    dicom_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    dicom_store_name = f"{dicom_store_parent}/dicomStores/{dicom_store_id}"

    body = {"gcsDestination": {"uriPrefix": f"gs://{uri_prefix}"}}

    request = (
        client.projects()
        .locations()
        .datasets()
        .dicomStores()
        .export(name=dicom_store_name, body=body)
    )

    response = request.execute()
    print(f"Exported DICOM instances to bucket: gs://{uri_prefix}")

    return response


# [END healthcare_export_dicom_instance_gcs]


# [START healthcare_import_dicom_instance]
def import_dicom_instance(
    project_id, location, dataset_id, dicom_store_id, content_uri
):
    """Imports data into the DICOM store by copying it from the specified
    source.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
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
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the DICOM store's parent dataset ID
    # dicom_store_id = 'my-dicom-store'  # replace with the DICOM store's ID
    # content_uri = 'my-bucket/*.dcm'  # replace with a Cloud Storage bucket and DCM files
    dicom_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    dicom_store_name = f"{dicom_store_parent}/dicomStores/{dicom_store_id}"

    body = {"gcsSource": {"uri": f"gs://{content_uri}"}}

    # Escape "import()" method keyword because "import"
    # is a reserved keyword in Python
    request = (
        client.projects()
        .locations()
        .datasets()
        .dicomStores()
        .import_(name=dicom_store_name, body=body)
    )

    response = request.execute()
    print(f"Imported DICOM instance: {content_uri}")

    return response


# [END healthcare_import_dicom_instance]


# [START healthcare_dicom_store_get_iam_policy]
def get_dicom_store_iam_policy(project_id, location, dataset_id, dicom_store_id):
    """Gets the IAM policy for the specified DICOM store.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
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
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the DICOM store's parent dataset ID
    # dicom_store_id = 'my-dicom-store'  # replace with the DICOM store's ID
    dicom_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    dicom_store_name = f"{dicom_store_parent}/dicomStores/{dicom_store_id}"

    request = (
        client.projects()
        .locations()
        .datasets()
        .dicomStores()
        .getIamPolicy(resource=dicom_store_name)
    )
    response = request.execute()

    print("etag: {}".format(response.get("name")))
    return response


# [END healthcare_dicom_store_get_iam_policy]


# [START healthcare_dicom_store_set_iam_policy]
def set_dicom_store_iam_policy(
    project_id, location, dataset_id, dicom_store_id, member, role, etag=None
):
    """Sets the IAM policy for the specified DICOM store.

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

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
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
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the DICOM store's parent dataset ID
    # dicom_store_id = 'my-dicom-store'  # replace with the DICOM store's ID
    # member = 'myemail@example.com'  # replace with an authorized member
    # role = 'roles/viewer'  # replace with a Healthcare API IAM role
    dicom_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    dicom_store_name = f"{dicom_store_parent}/dicomStores/{dicom_store_id}"

    policy = {"bindings": [{"role": role, "members": [member]}]}

    if etag is not None:
        policy["etag"] = etag

    request = (
        client.projects()
        .locations()
        .datasets()
        .dicomStores()
        .setIamPolicy(resource=dicom_store_name, body={"policy": policy})
    )
    response = request.execute()

    print("etag: {}".format(response.get("name")))
    print("bindings: {}".format(response.get("bindings")))
    return response


# [END healthcare_dicom_store_set_iam_policy]


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

    parser.add_argument("--location", default="us-central1", help="GCP location")

    parser.add_argument("--dataset_id", default=None, help="Name of dataset")

    parser.add_argument("--dicom_store_id", default=None, help="Name of DICOM store")

    parser.add_argument(
        "--pubsub_topic",
        default=None,
        help="The Cloud Pub/Sub topic that notifications of "
        "changes are published on",
    )

    parser.add_argument(
        "--uri_prefix",
        default=None,
        help="URI for a Google Cloud Storage directory to which result files"
        'should be written (e.g., "bucket-id/path/to/destination/dir").',
    )

    parser.add_argument(
        "--content_uri",
        default=None,
        help="URI for a Google Cloud Storage directory from which files"
        'should be imported (e.g., "bucket-id/path/to/destination/dir").',
    )

    parser.add_argument(
        "--export_format",
        choices=["FORMAT_UNSPECIFIED", "DICOM", "JSON_BIGQUERY_IMPORT"],
        default="DICOM",
        help="Specifies the output format. If the format is unspecified, the"
        "default functionality is to export to DICOM.",
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

    command.add_parser("create-dicom-store", help=create_dicom_store.__doc__)
    command.add_parser("delete-dicom-store", help=delete_dicom_store.__doc__)
    command.add_parser("get-dicom-store", help=get_dicom_store.__doc__)
    command.add_parser("list-dicom-stores", help=list_dicom_stores.__doc__)
    command.add_parser("patch-dicom-store", help=patch_dicom_store.__doc__)
    command.add_parser("get_iam_policy", help=get_dicom_store_iam_policy.__doc__)
    command.add_parser("set_iam_policy", help=set_dicom_store_iam_policy.__doc__)
    command.add_parser("export-dicom-store", help=export_dicom_instance.__doc__)
    command.add_parser("import-dicom-store", help=import_dicom_instance.__doc__)

    return parser.parse_args()


def run_command(args):
    """Calls the program using the specified command."""
    if args.project_id is None:
        print(
            "You must specify a project ID or set the "
            '"GOOGLE_CLOUD_PROJECT" environment variable.'
        )
        return

    elif args.command == "create-dicom-store":
        create_dicom_store(
            args.project_id, args.location, args.dataset_id, args.dicom_store_id
        )

    elif args.command == "delete-dicom-store":
        delete_dicom_store(
            args.project_id, args.location, args.dataset_id, args.dicom_store_id
        )

    elif args.command == "get-dicom-store":
        get_dicom_store(
            args.project_id, args.location, args.dataset_id, args.dicom_store_id
        )

    elif args.command == "list-dicom-stores":
        list_dicom_stores(args.project_id, args.location, args.dataset_id)

    elif args.command == "patch-dicom-store":
        patch_dicom_store(
            args.project_id,
            args.location,
            args.dataset_id,
            args.dicom_store_id,
            args.pubsub_topic,
        )

    elif args.command == "export-dicom-store":
        export_dicom_instance(
            args.project_id,
            args.location,
            args.dataset_id,
            args.dicom_store_id,
            args.uri_prefix,
        )

    elif args.command == "import-dicom-store":
        import_dicom_instance(
            args.project_id,
            args.location,
            args.dataset_id,
            args.dicom_store_id,
            args.content_uri,
        )

    elif args.command == "get_iam_policy":
        get_dicom_store_iam_policy(
            args.project_id, args.location, args.dataset_id, args.dicom_store_id
        )

    elif args.command == "set_iam_policy":
        set_dicom_store_iam_policy(
            args.project_id,
            args.location,
            args.dataset_id,
            args.dicom_store_id,
            args.member,
            args.role,
        )


def main():
    args = parse_command_line_args()
    run_command(args)


if __name__ == "__main__":
    main()
