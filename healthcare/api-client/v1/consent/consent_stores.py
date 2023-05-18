# Copyright 2022 Google LLC
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


# [START healthcare_create_consent_store]
def create_consent_store(
    project_id: str, location: str, dataset_id: str, consent_store_id: str
):
    """Creates a new consent store within the parent dataset.
    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/consent
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
    # dataset_id = 'my-dataset'  # replace with the consent store's parent dataset ID
    # consent_store_id = 'my-consent-store'  # replace with the consent store's ID
    consent_store_parent = (
        f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
    )

    request = (
        client.projects()
        .locations()
        .datasets()
        .consentStores()
        .create(parent=consent_store_parent, body={}, consentStoreId=consent_store_id)
    )

    response = request.execute()
    print(f"Created consent store: {consent_store_id}")
    return response


# [END healthcare_create_consent_store]


# [START healthcare_delete_consent_store]
def delete_consent_store(
    project_id: str, location: str, dataset_id: str, consent_store_id: str
):
    """Deletes the specified consent store.
    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/consent
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
    # dataset_id = 'my-dataset'  # replace with the consent store's parent dataset ID
    # consent_store_id = 'my-consent-store'  # replace with the consent store's ID
    consent_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    consent_store_name = "{}/consentStores/{}".format(
        consent_store_parent, consent_store_id
    )

    request = (
        client.projects()
        .locations()
        .datasets()
        .consentStores()
        .delete(name=consent_store_name)
    )

    response = request.execute()
    print(f"Deleted consent store: {consent_store_id}")
    return response


# [END healthcare_delete_consent_store]


# [START healthcare_get_consent_store]
def get_consent_store(
    project_id: str, location: str, dataset_id: str, consent_store_id: str
):
    """Gets the specified consent store.
    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/consent
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
    # dataset_id = 'my-dataset'  # replace with the consent store's parent dataset ID
    # consent_store_id = 'my-consent-store'  # replace with the consent store's ID
    consent_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    consent_store_name = "{}/consentStores/{}".format(
        consent_store_parent, consent_store_id
    )

    consent_stores = client.projects().locations().datasets().consentStores()
    consent_store = consent_stores.get(name=consent_store_name).execute()

    print(json.dumps(consent_store, indent=2))
    return consent_store


# [END healthcare_get_consent_store]


# [START healthcare_list_consent_stores]
def list_consent_stores(project_id, location, dataset_id):
    """Lists the consent stores in the given dataset.
    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/consent
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
    # dataset_id = 'my-dataset'  # replace with the consent store's parent dataset ID
    consent_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )

    consent_stores = (
        client.projects()
        .locations()
        .datasets()
        .consentStores()
        .list(parent=consent_store_parent)
        .execute()
        .get("consentStores", [])
    )

    for consent_store in consent_stores:
        print(consent_store)

    return consent_stores


# [END healthcare_list_consent_stores]


# [START healthcare_patch_consent_store]
def patch_consent_store(
    project_id: str,
    location: str,
    dataset_id: str,
    consent_store_id: str,
    default_consent_ttl,
):
    """Updates the consent store.
    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/consent
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
    # dataset_id = 'my-dataset'  # replace with the consent store's parent dataset ID
    # consent_store_id = 'my-consent-store'  # replace with the consent store's ID
    # default_consent_ttl = '172800s'  # replace with a default TTL
    consent_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    consent_store_name = "{}/consentStores/{}".format(
        consent_store_parent, consent_store_id
    )

    # Updates the default time-to-live (TTL) of consents in the consent store.
    # Updating the TTL does not affect the expiration time of existing consents.
    # Specify as a duration in seconds with up to nine fractional digits,
    # terminated by "s", for example "172800s".
    # Minimum value is 24 hours, or "86400s" in seconds.
    patch = {"defaultConsentTtl": default_consent_ttl}

    request = (
        client.projects()
        .locations()
        .datasets()
        .consentStores()
        .patch(name=consent_store_name, updateMask="defaultConsentTtl", body=patch)
    )

    response = request.execute()
    print(
        "Patched consent store {} with new default consent TTL: {}".format(
            consent_store_id, default_consent_ttl
        )
    )

    return response


# [END healthcare_patch_consent_store]


# [START healthcare_consent_store_get_iam_policy]
def get_consent_store_iam_policy(
    project_id: str, location: str, dataset_id: str, consent_store_id: str
):
    """Gets the IAM policy for the specified consent store.
    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/consent
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
    # dataset_id = 'my-dataset'  # replace with the consent store's parent dataset ID
    # consent_store_id = 'my-consent-store'  # replace with the consent store's ID
    consent_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    consent_store_name = "{}/consentStores/{}".format(
        consent_store_parent, consent_store_id
    )

    request = (
        client.projects()
        .locations()
        .datasets()
        .consentStores()
        .getIamPolicy(resource=consent_store_name)
    )
    response = request.execute()

    print("etag: {}".format(response.get("name")))
    return response


# [END healthcare_consent_store_get_iam_policy]


# [START healthcare_consent_store_set_iam_policy]
def set_consent_store_iam_policy(
    project_id: str,
    location: str,
    dataset_id: str,
    consent_store_id: str,
    member,
    role,
    etag=None,
):
    """Sets the IAM policy for the specified consent store.
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
    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/consent
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
    # dataset_id = 'my-dataset'  # replace with the consent store's parent dataset ID
    # consent_store_id = 'my-consent-store'  # replace with the consent store's ID
    # member = 'myemail@example.com'  # replace with an authorized member
    # role = 'roles/viewer'  # replace with a Healthcare API IAM role
    consent_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    consent_store_name = "{}/consentStores/{}".format(
        consent_store_parent, consent_store_id
    )

    policy = {"bindings": [{"role": role, "members": [member]}]}

    if etag is not None:
        policy["etag"] = etag

    request = (
        client.projects()
        .locations()
        .datasets()
        .consentStores()
        .setIamPolicy(resource=consent_store_name, body={"policy": policy})
    )
    response = request.execute()

    print("etag: {}".format(response.get("name")))
    print("bindings: {}".format(response.get("bindings")))
    return response


# [END healthcare_consent_store_set_iam_policy]


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

    parser.add_argument(
        "--consent_store_id", default=None, help="Name of consent store"
    )

    parser.add_argument(
        "--default_consent_ttl",
        default=None,
        help="Default time-to-live (TTL) of consents in the consent store.",
    )

    parser.add_argument(
        "--export_format",
        choices=["FORMAT_UNSPECIFIED", "consent", "JSON_BIGQUERY_IMPORT"],
        default="consent",
        help="Specifies the output format. If the format is unspecified, the"
        "default functionality is to export to consent.",
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

    command.add_parser("create-consent-store", help=create_consent_store.__doc__)
    command.add_parser("delete-consent-store", help=delete_consent_store.__doc__)
    command.add_parser("get-consent-store", help=get_consent_store.__doc__)
    command.add_parser("list-consent-stores", help=list_consent_stores.__doc__)
    command.add_parser("patch-consent-store", help=patch_consent_store.__doc__)
    command.add_parser("get_iam_policy", help=get_consent_store_iam_policy.__doc__)
    command.add_parser("set_iam_policy", help=set_consent_store_iam_policy.__doc__)

    return parser.parse_args()


def run_command(args):
    """Calls the program using the specified command."""
    if args.project_id is None:
        print(
            "You must specify a project ID or set the "
            '"GOOGLE_CLOUD_PROJECT" environment variable.'
        )
        return

    elif args.command == "create-consent-store":
        create_consent_store(
            args.project_id, args.location, args.dataset_id, args.consent_store_id
        )

    elif args.command == "delete-consent-store":
        delete_consent_store(
            args.project_id, args.location, args.dataset_id, args.consent_store_id
        )

    elif args.command == "get-consent-store":
        get_consent_store(
            args.project_id, args.location, args.dataset_id, args.consent_store_id
        )

    elif args.command == "list-consent-stores":
        list_consent_stores(args.project_id, args.location, args.dataset_id)

    elif args.command == "patch-consent-store":
        patch_consent_store(
            args.project_id,
            args.location,
            args.dataset_id,
            args.consent_store_id,
            args.default_consent_ttl,
        )

    elif args.command == "get_iam_policy":
        get_consent_store_iam_policy(
            args.project_id, args.location, args.dataset_id, args.consent_store_id
        )

    elif args.command == "set_iam_policy":
        set_consent_store_iam_policy(
            args.project_id,
            args.location,
            args.dataset_id,
            args.consent_store_id,
            args.member,
            args.role,
        )


def main():
    args = parse_command_line_args()
    run_command(args)


if __name__ == "__main__":
    main()
