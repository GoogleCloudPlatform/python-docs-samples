# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Demonstrates how to authenticate to Google Cloud Platform APIs using
the Google Cloud Client Libraries."""

import argparse


# [START auth_cloud_implicit]
def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)


# [END auth_cloud_implicit]


# [START auth_cloud_explicit]
def explicit():
    from google.cloud import storage

    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json("service_account.json")

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)


# [END auth_cloud_explicit]


# [START auth_cloud_explicit_compute_engine]
def explicit_compute_engine(project):
    from google.auth import compute_engine
    from google.cloud import storage

    # Explicitly use Compute Engine credentials. These credentials are
    # available on Compute Engine, App Engine Flexible, and Kubernetes Engine.
    credentials = compute_engine.Credentials()

    # Create the client using the credentials and specifying a project ID.
    storage_client = storage.Client(credentials=credentials, project=project)

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)


# [END auth_cloud_explicit_compute_engine]


# [START auth_cloud_accesstoken_impersonated_credentials]
def accesstoken_from_impersonated_credentials(
    impersonated_service_account: str, scope: str
):
    from google.auth import impersonated_credentials
    import google.auth.transport.requests

    """
      Use a service account (SA1) to impersonate another service account (SA2)
      and obtain an ID token for the impersonated account.
      To obtain a token for SA2, SA1 should have the
      "roles/iam.serviceAccountTokenCreator" permission on SA2.

    Args:
        impersonated_service_account: The name of the privilege-bearing service account for whom the credential is created.
            Examples: name@project.service.gserviceaccount.com

        scope: Provide the scopes that you might need to request to access Google APIs,
            depending on the level of access you need.
            For this example, we use the cloud-wide scope and use IAM to narrow the permissions.
            https://cloud.google.com/docs/authentication#authorization_for_services
            For more information, see: https://developers.google.com/identity/protocols/oauth2/scopes
    """

    # Construct the GoogleCredentials object which obtains the default configuration from your
    # working environment.
    credentials, project_id = google.auth.default()

    # Create the impersonated credential.
    target_credentials = impersonated_credentials.Credentials(
        source_credentials=credentials,
        target_principal=impersonated_service_account,
        # delegates: The chained list of delegates required to grant the final accessToken.
        # For more information, see:
        # https://cloud.google.com/iam/docs/create-short-lived-credentials-direct#sa-credentials-permissions
        # Delegate is NOT USED here.
        delegates=[],
        target_scopes=[scope],
        lifetime=300,
    )

    # Get the OAuth2 token.
    # Once you've obtained the OAuth2 token, use it to make an authenticated call
    # to the target audience.
    request = google.auth.transport.requests.Request()
    target_credentials.refresh(request)
    # The token field is target_credentials.token.
    print("Generated OAuth2 token.")


# [END auth_cloud_accesstoken_impersonated_credentials]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("implicit", help=implicit.__doc__)
    subparsers.add_parser("explicit", help=explicit.__doc__)
    explicit_gce_parser = subparsers.add_parser(
        "explicit_compute_engine", help=explicit_compute_engine.__doc__
    )
    explicit_gce_parser.add_argument("project")
    accesstoken_parser = subparsers.add_parser(
        "accesstoken_from_impersonated_credentials",
        help=accesstoken_from_impersonated_credentials.__doc__,
    )
    accesstoken_parser.add_argument("impersonated_service_account")
    accesstoken_parser.add_argument("scope")

    args = parser.parse_args()

    if args.command == "implicit":
        implicit()
    elif args.command == "explicit":
        explicit()
    elif args.command == "explicit_compute_engine":
        explicit_compute_engine(args.project)
    elif args.command == "accesstoken_from_impersonated_credentials":
        accesstoken_from_impersonated_credentials(
            args.impersonated_service_account, args.scope
        )
