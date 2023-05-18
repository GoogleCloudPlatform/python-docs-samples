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


# [START healthcare_create_hl7v2_message]
def create_hl7v2_message(
    project_id, location, dataset_id, hl7v2_store_id, hl7v2_message_file
):
    """Creates an HL7v2 message and sends a notification to the
    Cloud Pub/Sub topic.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/hl7v2
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
    # dataset_id = 'my-dataset'  # replace with the HL7v2 store's parent dataset ID
    # hl7v2_store_id = 'my-hl7v2-store'  # replace with the HL7v2 store's ID
    # hl7v2_message_file = 'hl7v2-message.json'  # replace with the path to the HL7v2 file
    hl7v2_parent = f"projects/{project_id}/locations/{location}"
    hl7v2_store_name = "{}/datasets/{}/hl7V2Stores/{}".format(
        hl7v2_parent, dataset_id, hl7v2_store_id
    )

    with open(hl7v2_message_file) as hl7v2_message:
        hl7v2_message_content = json.load(hl7v2_message)

    request = (
        client.projects()
        .locations()
        .datasets()
        .hl7V2Stores()
        .messages()
        .create(parent=hl7v2_store_name, body=hl7v2_message_content)
    )

    response = request.execute()
    print(f"Created HL7v2 message from file: {hl7v2_message_file}")
    return response


# [END healthcare_create_hl7v2_message]


# [START healthcare_delete_hl7v2_message]
def delete_hl7v2_message(
    project_id, location, dataset_id, hl7v2_store_id, hl7v2_message_id
):
    """Deletes an HL7v2 message.

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
    # hl7v2_message_id = '2yqbdhYHlk_ucSmWkcKOVm_N0p0OpBXgIlVG18rB-cw='  # replace with the HL7v2 message ID that was returned by the server
    hl7v2_parent = f"projects/{project_id}/locations/{location}"
    hl7v2_message = "{}/datasets/{}/hl7V2Stores/{}/messages/{}".format(
        hl7v2_parent, dataset_id, hl7v2_store_id, hl7v2_message_id
    )

    request = (
        client.projects()
        .locations()
        .datasets()
        .hl7V2Stores()
        .messages()
        .delete(name=hl7v2_message)
    )

    response = request.execute()
    print(f"Deleted HL7v2 message with ID: {hl7v2_message_id}")
    return response


# [END healthcare_delete_hl7v2_message]


# [START healthcare_get_hl7v2_message]
def get_hl7v2_message(
    project_id, location, dataset_id, hl7v2_store_id, hl7v2_message_id
):
    """Gets an HL7v2 message.

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
    # hl7v2_message_id = '2yqbdhYHlk_ucSmWkcKOVm_N0p0OpBXgIlVG18rB-cw='  # replace with the HL7v2 message ID that was returned by the server
    hl7v2_parent = f"projects/{project_id}/locations/{location}"
    hl7v2_message_name = "{}/datasets/{}/hl7V2Stores/{}/messages/{}".format(
        hl7v2_parent, dataset_id, hl7v2_store_id, hl7v2_message_id
    )

    msgs = client.projects().locations().datasets().hl7V2Stores().messages()
    message = msgs.get(name=hl7v2_message_name).execute()

    print("Name: {}".format(message.get("name")))
    print("Data: {}".format(message.get("data")))
    print("Creation time: {}".format(message.get("createTime")))
    print("Sending facility: {}".format(message.get("sendFacility")))
    print("Time sent: {}".format(message.get("sendTime")))
    print("Message type: {}".format(message.get("messageType")))
    print("Patient IDs:")
    patient_ids = message.get("patientIds")
    for patient_id in patient_ids:
        print("\tPatient value: {}".format(patient_id.get("value")))
        print("\tPatient type: {}".format(patient_id.get("type")))
    print("Labels: {}".format(message.get("labels")))

    print(message)
    return message


# [END healthcare_get_hl7v2_message]


# [START healthcare_ingest_hl7v2_message]
def ingest_hl7v2_message(
    project_id, location, dataset_id, hl7v2_store_id, hl7v2_message_file
):
    """Ingests a new HL7v2 message from the hospital and sends a notification
    to the Cloud Pub/Sub topic. Return is an HL7v2 ACK message if the message
    was successfully stored.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/hl7v2
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
    # dataset_id = 'my-dataset'  # replace with the HL7v2 store's parent dataset ID
    # hl7v2_store_id = 'my-hl7v2-store'  # replace with the HL7v2 store's ID
    # hl7v2_message_file = 'hl7v2-message.json'  # replace with the path to the HL7v2 file
    hl7v2_parent = f"projects/{project_id}/locations/{location}"
    hl7v2_store_name = "{}/datasets/{}/hl7V2Stores/{}".format(
        hl7v2_parent, dataset_id, hl7v2_store_id
    )

    with open(hl7v2_message_file) as hl7v2_message:
        hl7v2_message_content = json.load(hl7v2_message)

    request = (
        client.projects()
        .locations()
        .datasets()
        .hl7V2Stores()
        .messages()
        .ingest(parent=hl7v2_store_name, body=hl7v2_message_content)
    )

    response = request.execute()
    print(f"Ingested HL7v2 message from file: {hl7v2_message_file}")
    return response


# [END healthcare_ingest_hl7v2_message]


# [START healthcare_list_hl7v2_messages]
def list_hl7v2_messages(project_id, location, dataset_id, hl7v2_store_id):
    """Lists all the messages in the given HL7v2 store with support for
    filtering.

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
    hl7v2_messages_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    hl7v2_message_path = "{}/hl7V2Stores/{}".format(
        hl7v2_messages_parent, hl7v2_store_id
    )

    hl7v2_messages = (
        client.projects()
        .locations()
        .datasets()
        .hl7V2Stores()
        .messages()
        .list(parent=hl7v2_message_path)
        .execute()
        .get("hl7V2Messages", [])
    )

    for hl7v2_message in hl7v2_messages:
        print(hl7v2_message)

    return hl7v2_messages


# [END healthcare_list_hl7v2_messages]


# [START healthcare_patch_hl7v2_message]
def patch_hl7v2_message(
    project_id,
    location,
    dataset_id,
    hl7v2_store_id,
    hl7v2_message_id,
    label_key,
    label_value,
):
    """Updates the message.

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
    # hl7v2_message_id = '2yqbdhYHlk_ucSmWkcKOVm_N0p0OpBXgIlVG18rB-cw='  # replace with the HL7v2 message ID that was returned by the server
    # label_key = 'key1'  # replace with a key
    # label_value = 'label2'  # replace with a key value
    hl7v2_message_parent = f"projects/{project_id}/locations/{location}"
    hl7v2_message_name = "{}/datasets/{}/hl7V2Stores/{}/messages/{}".format(
        hl7v2_message_parent, dataset_id, hl7v2_store_id, hl7v2_message_id
    )

    patch = {"labels": {label_key: label_value}}

    request = (
        client.projects()
        .locations()
        .datasets()
        .hl7V2Stores()
        .messages()
        .patch(name=hl7v2_message_name, updateMask="labels", body=patch)
    )

    response = request.execute()
    print(
        "Patched HL7v2 message {} with labels:\n\t{}: {}".format(
            hl7v2_message_id, label_key, label_value
        )
    )
    return response


# [END healthcare_patch_hl7v2_message]


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
        "--hl7v2_message_file",
        default=None,
        help="A file containing a base64-encoded HL7v2 message",
    )

    parser.add_argument(
        "--hl7v2_message_id",
        default=None,
        help="The identifier for the message returned by the server",
    )

    parser.add_argument(
        "--label_key", default=None, help="Arbitrary label key to apply to the message"
    )

    parser.add_argument(
        "--label_value",
        default=None,
        help="Arbitrary label value to apply to the message",
    )

    command = parser.add_subparsers(dest="command")

    command.add_parser("create-hl7v2-message", help=create_hl7v2_message.__doc__)
    command.add_parser("delete-hl7v2-message", help=delete_hl7v2_message.__doc__)
    command.add_parser("get-hl7v2-message", help=get_hl7v2_message.__doc__)
    command.add_parser("ingest-hl7v2-message", help=ingest_hl7v2_message.__doc__)
    command.add_parser("list-hl7v2-messages", help=list_hl7v2_messages.__doc__)
    command.add_parser("patch-hl7v2-message", help=patch_hl7v2_message.__doc__)

    return parser.parse_args()


def run_command(args):
    """Calls the program using the specified command."""
    if args.project_id is None:
        print(
            "You must specify a project ID or set the "
            '"GOOGLE_CLOUD_PROJECT" environment variable.'
        )
        return

    elif args.command == "create-hl7v2-message":
        create_hl7v2_message(
            args.project_id,
            args.location,
            args.dataset_id,
            args.hl7v2_store_id,
            args.hl7v2_message_file,
        )

    elif args.command == "delete-hl7v2-message":
        delete_hl7v2_message(
            args.project_id,
            args.location,
            args.dataset_id,
            args.hl7v2_store_id,
            args.hl7v2_message_id,
        )

    elif args.command == "get-hl7v2-message":
        get_hl7v2_message(
            args.project_id,
            args.location,
            args.dataset_id,
            args.hl7v2_store_id,
            args.hl7v2_message_id,
        )

    elif args.command == "ingest-hl7v2-message":
        ingest_hl7v2_message(
            args.project_id,
            args.location,
            args.dataset_id,
            args.hl7v2_store_id,
            args.hl7v2_message_file,
        )

    elif args.command == "list-hl7v2-messages":
        list_hl7v2_messages(
            args.project_id, args.location, args.dataset_id, args.hl7v2_store_id
        )

    elif args.command == "patch-hl7v2-message":
        patch_hl7v2_message(
            args.project_id,
            args.location,
            args.dataset_id,
            args.hl7v2_store_id,
            args.hl7v2_message_id,
            args.label_key,
            args.label_value,
        )


def main():
    args = parse_command_line_args()
    run_command(args)


if __name__ == "__main__":
    main()
