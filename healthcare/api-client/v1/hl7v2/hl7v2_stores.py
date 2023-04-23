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


# [START healthcare_create_hl7v2_store]
def create_hl7v2_store(project_id, location, dataset_id, hl7v2_store_id):
    """Creates a new HL7v2 store within the parent dataset.
    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/hl7v2
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
    # dataset_id = 'my-dataset'  # replace with the HL7v2 store's parent dataset ID
    # hl7v2_store_id = 'my-hl7v2-store'  # replace with the HL7v2 store's ID
    hl7v2_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )

    request = (
        client.projects()
        .locations()
        .datasets()
        .hl7V2Stores()
        .create(parent=hl7v2_store_parent, body={}, hl7V2StoreId=hl7v2_store_id)
    )

    response = request.execute()
    print(f"Created HL7v2 store: {hl7v2_store_id}")
    return response


# [END healthcare_create_hl7v2_store]


# [START healthcare_delete_hl7v2_store]
def delete_hl7v2_store(project_id, location, dataset_id, hl7v2_store_id):
    """Deletes the specified HL7v2 store.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/hl7v2
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
    # dataset_id = 'my-dataset'  # replace with the HL7v2 store's parent dataset
    # hl7v2_store_id = 'my-hl7v2-store'  # replace with the HL7v2 store's ID
    hl7v2_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    hl7v2_store_name = f"{hl7v2_store_parent}/hl7V2Stores/{hl7v2_store_id}"

    request = (
        client.projects()
        .locations()
        .datasets()
        .hl7V2Stores()
        .delete(name=hl7v2_store_name)
    )

    response = request.execute()
    print(f"Deleted HL7v2 store: {hl7v2_store_id}")
    return response


# [END healthcare_delete_hl7v2_store]


# [START healthcare_get_hl7v2_store]
def get_hl7v2_store(project_id, location, dataset_id, hl7v2_store_id):
    """Gets the specified HL7v2 store.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/hl7v2
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
    # dataset_id = 'my-dataset'  # replace with the HL7v2 store's parent dataset
    # hl7v2_store_id = 'my-hl7v2-store'  # replace with the HL7v2 store's ID
    hl7v2_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    hl7v2_store_name = f"{hl7v2_store_parent}/hl7V2Stores/{hl7v2_store_id}"

    hl7v2_stores = client.projects().locations().datasets().hl7V2Stores()
    hl7v2_store = hl7v2_stores.get(name=hl7v2_store_name).execute()

    print("Name: {}".format(hl7v2_store.get("name")))
    if hl7v2_store.get("notificationConfigs") is not None:
        print("Notification configs:")
        for notification_config in hl7v2_store.get("notificationConfigs"):
            print(
                "\tPub/Sub topic: {}".format(notification_config.get("pubsubTopic")),
                "\tFilter: {}".format(notification_config.get("filter")),
            )

    return hl7v2_store


# [END healthcare_get_hl7v2_store]


# [START healthcare_list_hl7v2_stores]
def list_hl7v2_stores(project_id, location, dataset_id):
    """Lists the HL7v2 stores in the given dataset.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/hl7v2
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
    # dataset_id = 'my-dataset'  # replace with the HL7v2 store's parent dataset
    hl7v2_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )

    hl7v2_stores = (
        client.projects()
        .locations()
        .datasets()
        .hl7V2Stores()
        .list(parent=hl7v2_store_parent)
        .execute()
        .get("hl7V2Stores", [])
    )

    for hl7v2_store in hl7v2_stores:
        print("HL7v2 store:\nName: {}".format(hl7v2_store.get("name")))
        if hl7v2_store.get("notificationConfigs") is not None:
            print("Notification configs:")
            for notification_config in hl7v2_store.get("notificationConfigs"):
                print(
                    "\tPub/Sub topic: {}".format(
                        notification_config.get("pubsubTopic")
                    ),
                    "\tFilter: {}".format(notification_config.get("filter")),
                )
    return hl7v2_stores


# [END healthcare_list_hl7v2_stores]


# [START healthcare_patch_hl7v2_store]
def patch_hl7v2_store(project_id, location, dataset_id, hl7v2_store_id):
    """Updates the HL7v2 store.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/hl7v2
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
    # dataset_id = 'my-dataset'  # replace with the HL7v2 store's parent dataset
    # hl7v2_store_id = 'my-hl7v2-store'  # replace with the HL7v2 store's ID
    hl7v2_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    hl7v2_store_name = f"{hl7v2_store_parent}/hl7V2Stores/{hl7v2_store_id}"

    # TODO(developer): Replace with the full URI of an existing Pub/Sub topic
    patch = {"notificationConfigs": None}

    request = (
        client.projects()
        .locations()
        .datasets()
        .hl7V2Stores()
        .patch(name=hl7v2_store_name, updateMask="notificationConfigs", body=patch)
    )

    response = request.execute()
    print(
        f"Patched HL7v2 store {hl7v2_store_id} with Cloud Pub/Sub topic: None"
    )
    return response


# [END healthcare_patch_hl7v2_store]


# [START healthcare_hl7v2_store_get_iam_policy]
def get_hl7v2_store_iam_policy(project_id, location, dataset_id, hl7v2_store_id):
    """Gets the IAM policy for the specified HL7v2 store.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/hl7v2
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
    # dataset_id = 'my-dataset'  # replace with the HL7v2 store's parent dataset
    # hl7v2_store_id = 'my-hl7v2-store'  # replace with the HL7v2 store's ID
    hl7v2_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    hl7v2_store_name = f"{hl7v2_store_parent}/hl7V2Stores/{hl7v2_store_id}"

    request = (
        client.projects()
        .locations()
        .datasets()
        .hl7V2Stores()
        .getIamPolicy(resource=hl7v2_store_name)
    )
    response = request.execute()

    print("etag: {}".format(response.get("name")))
    return response


# [END healthcare_hl7v2_store_get_iam_policy]


# [START healthcare_hl7v2_store_set_iam_policy]
def set_hl7v2_store_iam_policy(
    project_id, location, dataset_id, hl7v2_store_id, member, role, etag=None
):
    """Sets the IAM policy for the specified HL7v2 store.
        A single member will be assigned a single role. A member can be any of:
        - allUsers, that is, anyone
        - allAuthenticatedUsers, anyone authenticated with a Google account
        - user:email, as in 'user:somebody@example.com'
        - group:email, as in 'group:admins@example.com'
        - domain:domainname, as in 'domain:example.com'
        - serviceAccount:email,
            as in 'serviceAccount:my-other-app@appspot.gserviceaccount.com'
        A role can be any IAM role, such as 'roles/viewer', 'roles/owner',
        or 'roles/editor'.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/hl7v2
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
    # dataset_id = 'my-dataset'  # replace with the HL7v2 store's parent dataset
    # hl7v2_store_id = 'my-hl7v2-store'  # replace with the HL7v2 store's ID
    # member = 'myemail@example.com'  # replace with an authorized member
    # role = 'roles/viewer'  # replace with a Healthcare API IAM role
    hl7v2_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    hl7v2_store_name = f"{hl7v2_store_parent}/hl7V2Stores/{hl7v2_store_id}"

    policy = {"bindings": [{"role": role, "members": [member]}]}

    if etag is not None:
        policy["etag"] = etag

    request = (
        client.projects()
        .locations()
        .datasets()
        .hl7V2Stores()
        .setIamPolicy(resource=hl7v2_store_name, body={"policy": policy})
    )
    response = request.execute()

    print("etag: {}".format(response.get("name")))
    print("bindings: {}".format(response.get("bindings")))
    return response


# [END healthcare_hl7v2_store_set_iam_policy]


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

    parser.add_argument("--hl7v2_store_id", default=None, help="Name of HL7v2 store")

    parser.add_argument(
        "--pubsub_topic",
        default=None,
        help="The Cloud Pub/Sub topic where notifications of changes " "are published",
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

    command.add_parser("create-hl7v2-store", help=create_hl7v2_store.__doc__)
    command.add_parser("delete-hl7v2-store", help=delete_hl7v2_store.__doc__)
    command.add_parser("get-hl7v2-store", help=get_hl7v2_store.__doc__)
    command.add_parser("list-hl7v2-stores", help=list_hl7v2_stores.__doc__)
    command.add_parser("patch-hl7v2-store", help=patch_hl7v2_store.__doc__)
    command.add_parser("get_iam_policy", help=get_hl7v2_store_iam_policy.__doc__)
    command.add_parser("set_iam_policy", help=set_hl7v2_store_iam_policy.__doc__)

    return parser.parse_args()


def run_command(args):
    """Calls the program using the specified command."""
    if args.project_id is None:
        print(
            "You must specify a project ID or set the "
            '"GOOGLE_CLOUD_PROJECT" environment variable.'
        )
        return

    elif args.command == "create-hl7v2-store":
        create_hl7v2_store(
            args.project_id, args.location, args.dataset_id, args.hl7v2_store_id
        )

    elif args.command == "delete-hl7v2-store":
        delete_hl7v2_store(
            args.project_id, args.location, args.dataset_id, args.hl7v2_store_id
        )

    elif args.command == "get-hl7v2-store":
        get_hl7v2_store(
            args.project_id, args.location, args.dataset_id, args.hl7v2_store_id
        )

    elif args.command == "list-hl7v2-stores":
        list_hl7v2_stores(args.project_id, args.location, args.dataset_id)

    elif args.command == "patch-hl7v2-store":
        patch_hl7v2_store(
            args.project_id,
            args.location,
            args.dataset_id,
            args.hl7v2_store_id,
            args.pubsub_topic,
        )

    elif args.command == "get_hl7v2_store_iam_policy":
        get_hl7v2_store_iam_policy(
            args.project_id, args.location, args.dataset_id, args.hl7v2_store_id
        )

    elif args.command == "set_hl7v2_store_iam_policy":
        set_hl7v2_store_iam_policy(
            args.project_id,
            args.location,
            args.dataset_id,
            args.hl7v2_store_id,
            args.member,
            args.role,
        )


def main():
    args = parse_command_line_args()
    run_command(args)


if __name__ == "__main__":
    main()
