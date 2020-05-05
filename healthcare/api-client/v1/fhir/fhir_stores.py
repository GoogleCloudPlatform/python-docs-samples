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

from googleapiclient import discovery


# [START healthcare_get_client]
def get_client():
    """Returns an authorized API client.

    Discovers the Healthcare API and
    creates a service object using the service account credentials in the
    GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    api_version = "v1"
    service_name = "healthcare"

    return discovery.build(service_name, api_version)
# [END healthcare_get_client]


# [START healthcare_create_fhir_store]
def create_fhir_store(project_id, cloud_region, dataset_id, fhir_store_id):
    """Creates a new FHIR store within the parent dataset."""
    client = get_client()
    fhir_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, cloud_region, dataset_id
    )

    body = {"version": "STU3"}

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .create(parent=fhir_store_parent, body=body, fhirStoreId=fhir_store_id)
    )

    response = request.execute()
    print("Created FHIR store: {}".format(fhir_store_id))

    return response


# [END healthcare_create_fhir_store]


# [START healthcare_delete_fhir_store]
def delete_fhir_store(project_id, cloud_region, dataset_id, fhir_store_id):
    """Deletes the specified FHIR store."""
    client = get_client()
    fhir_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, cloud_region, dataset_id
    )
    fhir_store_name = "{}/fhirStores/{}".format(fhir_store_parent, fhir_store_id)

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .delete(name=fhir_store_name)
    )

    response = request.execute()
    print("Deleted FHIR store: {}".format(fhir_store_id))

    return response


# [END healthcare_delete_fhir_store]


# [START healthcare_get_fhir_store]
def get_fhir_store(project_id, cloud_region, dataset_id, fhir_store_id):
    """Gets the specified FHIR store."""
    client = get_client()
    fhir_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, cloud_region, dataset_id
    )
    fhir_store_name = "{}/fhirStores/{}".format(fhir_store_parent, fhir_store_id)

    fhir_stores = client.projects().locations().datasets().fhirStores()
    fhir_store = fhir_stores.get(name=fhir_store_name).execute()

    print(json.dumps(fhir_store, indent=2))
    return fhir_store


# [END healthcare_get_fhir_store]


# [START healthcare_get_metadata]
def get_fhir_store_metadata(project_id, cloud_region, dataset_id, fhir_store_id):
    """Gets the FHIR capability statement (STU3, R4), or the conformance statement
    in the DSTU2 case for the store, which contains a description of functionality
    supported by the server.
    """
    client = get_client()
    fhir_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, cloud_region, dataset_id
    )
    fhir_store_name = "{}/fhirStores/{}".format(fhir_store_parent, fhir_store_id)

    fhir_stores = client.projects().locations().datasets().fhirStores()
    response = fhir_stores.fhir().capabilities(name=fhir_store_name).execute()

    print(json.dumps(response, indent=2))
    return response


# [END healthcare_get_metadata]


# [START healthcare_list_fhir_stores]
def list_fhir_stores(project_id, cloud_region, dataset_id):
    """Lists the FHIR stores in the given dataset."""
    client = get_client()
    fhir_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, cloud_region, dataset_id
    )

    fhir_stores = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .list(parent=fhir_store_parent)
        .execute()
        .get("fhirStores", [])
    )

    for fhir_store in fhir_stores:
        print(fhir_store)

    return fhir_stores


# [END healthcare_list_fhir_stores]


# [START healthcare_patch_fhir_store]
def patch_fhir_store(project_id, cloud_region, dataset_id, fhir_store_id):
    """Updates the FHIR store."""
    client = get_client()
    fhir_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, cloud_region, dataset_id
    )
    fhir_store_name = "{}/fhirStores/{}".format(fhir_store_parent, fhir_store_id)

    patch = {"notificationConfig": None}

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .patch(name=fhir_store_name, updateMask="notificationConfig", body=patch)
    )

    response = request.execute()
    print("Patched FHIR store {} with Cloud Pub/Sub topic: None".format(fhir_store_id))

    return response


# [END healthcare_patch_fhir_store]


# [START healthcare_export_fhir_resources_gcs]
def export_fhir_store_gcs(project_id, cloud_region, dataset_id, fhir_store_id, gcs_uri):
    """Export resources to a Google Cloud Storage bucket by copying
    them from the FHIR store."""
    client = get_client()
    fhir_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, cloud_region, dataset_id
    )
    fhir_store_name = "{}/fhirStores/{}".format(fhir_store_parent, fhir_store_id)

    body = {"gcsDestination": {"uriPrefix": "gs://{}/fhir_export".format(gcs_uri)}}

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .export(name=fhir_store_name, body=body)
    )

    response = request.execute()
    print("Exported FHIR resources to bucket: gs://{}".format(gcs_uri))

    return response


# [END healthcare_export_fhir_resources_gcs]


# [START healthcare_import_fhir_resources]
def import_fhir_resources(project_id, cloud_region, dataset_id, fhir_store_id, gcs_uri):
    """Import resources into the FHIR store by copying them from the
    specified source.
    """
    client = get_client()
    fhir_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, cloud_region, dataset_id
    )
    fhir_store_name = "{}/fhirStores/{}".format(fhir_store_parent, fhir_store_id)

    body = {
        "contentStructure": "CONTENT_STRUCTURE_UNSPECIFIED",
        "gcsSource": {"uri": "gs://{}".format(gcs_uri)},
    }

    # Escape "import()" method keyword because "import"
    # is a reserved keyword in Python
    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .import_(name=fhir_store_name, body=body)
    )

    response = request.execute()
    print("Imported FHIR resources: {}".format(gcs_uri))

    return response


# [END healthcare_import_fhir_resources]


# [START healthcare_fhir_store_get_iam_policy]
def get_fhir_store_iam_policy(project_id, cloud_region, dataset_id, fhir_store_id):
    """Gets the IAM policy for the specified FHIR store."""
    client = get_client()
    fhir_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, cloud_region, dataset_id
    )
    fhir_store_name = "{}/fhirStores/{}".format(fhir_store_parent, fhir_store_id)

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .getIamPolicy(resource=fhir_store_name)
    )
    response = request.execute()

    print("etag: {}".format(response.get("name")))
    return response


# [END healthcare_fhir_store_get_iam_policy]


# [START healthcare_fhir_store_set_iam_policy]
def set_fhir_store_iam_policy(
    project_id, cloud_region, dataset_id, fhir_store_id, member, role, etag=None,
):
    """Sets the IAM policy for the specified FHIR store.
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
    """
    client = get_client()
    fhir_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, cloud_region, dataset_id
    )
    fhir_store_name = "{}/fhirStores/{}".format(fhir_store_parent, fhir_store_id)

    policy = {"bindings": [{"role": role, "members": [member]}]}

    if etag is not None:
        policy["etag"] = etag

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .setIamPolicy(resource=fhir_store_name, body={"policy": policy})
    )
    response = request.execute()

    print("etag: {}".format(response.get("name")))
    print("bindings: {}".format(response.get("bindings")))
    return response


# [END healthcare_fhir_store_set_iam_policy]


def parse_command_line_args():
    """Parses command line arguments."""

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--project_id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        help="GCP cloud project name",
    )

    parser.add_argument(
        "--cloud_region", default="us-central1", help="GCP cloud region"
    )

    parser.add_argument("--dataset_id", default=None, help="Name of dataset")

    parser.add_argument("--fhir_store_id", default=None, help="Name of FHIR store")

    parser.add_argument(
        "--pubsub_topic",
        default=None,
        help="The Cloud Pub/Sub topic where notifications of changes " "are published",
    )

    parser.add_argument(
        "--gcs_uri",
        default=None,
        help="URI for a Google Cloud Storage directory from which files"
        "should be import or to which result files"
        'should be written (e.g., "bucket-id/path/to/destination/dir").',
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

    command.add_parser("create-fhir-store", help=create_fhir_store.__doc__)
    command.add_parser("delete-fhir-store", help=delete_fhir_store.__doc__)
    command.add_parser("get-fhir-store", help=get_fhir_store.__doc__)
    command.add_parser("get-fhir-store-metadata", help=get_fhir_store_metadata.__doc__)
    command.add_parser("list-fhir-stores", help=list_fhir_stores.__doc__)
    command.add_parser("patch-fhir-store", help=patch_fhir_store.__doc__)
    command.add_parser("import-fhir-resources", help=import_fhir_resources.__doc__)
    command.add_parser("export-fhir-store-gcs", help=export_fhir_store_gcs.__doc__)
    command.add_parser("get_iam_policy", help=get_fhir_store_iam_policy.__doc__)
    command.add_parser("set_iam_policy", help=set_fhir_store_iam_policy.__doc__)

    return parser.parse_args()


def run_command(args):
    """Calls the program using the specified command."""
    if args.project_id is None:
        print(
            "You must specify a project ID or set the "
            '"GOOGLE_CLOUD_PROJECT" environment variable.'
        )
        return

    elif args.command == "create-fhir-store":
        create_fhir_store(
            args.project_id, args.cloud_region, args.dataset_id, args.fhir_store_id,
        )

    elif args.command == "delete-fhir-store":
        delete_fhir_store(
            args.project_id, args.cloud_region, args.dataset_id, args.fhir_store_id,
        )

    elif args.command == "get-fhir-store":
        get_fhir_store(
            args.project_id, args.cloud_region, args.dataset_id, args.fhir_store_id,
        )

    elif args.command == "get-fhir-store-metadata":
        get_fhir_store_metadata(
            args.project_id, args.cloud_region, args.dataset_id, args.fhir_store_id,
        )

    elif args.command == "list-fhir-stores":
        list_fhir_stores(
            args.project_id, args.cloud_region, args.dataset_id,
        )

    elif args.command == "patch-fhir-store":
        patch_fhir_store(
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.pubsub_topic,
        )

    elif args.command == "export-fhir-store-gcs":
        export_fhir_store_gcs(
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.gcs_uri,
        )

    elif args.command == "import-fhir-resources":
        import_fhir_resources(
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.gcs_uri,
        )

    elif args.command == "get_iam_policy":
        get_fhir_store_iam_policy(
            args.project_id, args.cloud_region, args.dataset_id, args.fhir_store_id,
        )

    elif args.command == "set_iam_policy":
        set_fhir_store_iam_policy(
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.member,
            args.role,
        )


def main():
    args = parse_command_line_args()
    run_command(args)


if __name__ == "__main__":
    main()
