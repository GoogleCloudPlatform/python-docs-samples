# Copyright 2025 Google LLC
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

# [START connectgateway_get_namespace]
import os
import sys
from google.auth.transport import requests
from google.cloud.gkeconnect import gateway_v1
from google.oauth2 import service_account
from kubernetes import client
from google.api_core import exceptions

# --- Configuration ---

SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

def get_gateway_url(membership_name: str, location: str) -> str:
    """Fetches the GKE Connect Gateway URL for the specified membership."""
    try:
        client_options = {}
        if location != "global":
            # If the location is not global, the endpoint needs to be set to the regional endpoint.
            regional_endpoint = f"{location}-connectgateway.googleapis.com"
            client_options = {"api_endpoint": regional_endpoint}
        gateway_client = gateway_v1.GatewayControlClient(client_options=client_options)
        request = gateway_v1.GenerateCredentialsRequest()
        request.name = membership_name
        response = gateway_client.generate_credentials(request=request)
        print(f'GKE Connect Gateway Endpoint: {response.endpoint}')
        if not response.endpoint:
            print("Error: GKE Connect Gateway Endpoint is empty.")
            sys.exit(1)
        return response.endpoint
    except exceptions.NotFound as e:
        print(f'Membership not found: {e}')
        sys.exit(1)
    except Exception as e:
        print(f'Error fetching GKE Connect Gateway URL: {e}')
        sys.exit(1)

def configure_kubernetes_client(gateway_url: str, service_account_key_path: str) -> client.CoreV1Api:
    """Configures the Kubernetes client with the GKE Connect Gateway URL and credentials."""

    configuration = client.Configuration()

    # Configure the API client with the custom host.
    configuration.host = gateway_url

    # Set the authentication header with the GCP OAuth token
    if not service_account_key_path:
        print("Error: SERVICE_ACCOUNT_KEY_PATH environment variable not set.")
        sys.exit(1)
    try:
        credentials = service_account.Credentials.from_service_account_file(
            service_account_key_path, scopes=SCOPES
        )
    except FileNotFoundError:
        print(f"Error: Service account key file not found at {service_account_key_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading service account credentials: {e}")
        sys.exit(1)
    auth_req = requests.Request()
    credentials.refresh(auth_req)
    configuration.api_key = {'authorization': f'Bearer {credentials.token}'}

    api_client = client.ApiClient(configuration=configuration)
    return client.CoreV1Api(api_client)

def get_default_namespace(api_client: client.CoreV1Api):
    """Get default namespace in the Kubernetes cluster."""
    try:
        namespace = api_client.read_namespace(name="default")
        if namespace is not None:
            print(f"\nDefault Namespace:\n{namespace}")
        else:
            print("Default namespace not found in the cluster.")
    except client.ApiException as e:
        print(f"Error getting default namespace: {e}\nStatus: {e.status}\nReason: {e.reason}")

def get_namespace(membership_name: str, location: str, service_account_key_path: str):
    """Main function to connect to the cluster and get the default namespace."""
    gateway_url = get_gateway_url(membership_name, location)
    core_v1_api = configure_kubernetes_client(gateway_url, service_account_key_path)
    get_default_namespace(core_v1_api)

# [END connectgateway_get_namespace]

if __name__ == "__main__":
    MEMBERSHIP_NAME = os.environ.get('MEMBERSHIP_NAME')
    SERVICE_ACCOUNT_KEY_PATH = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    get_namespace(MEMBERSHIP_NAME, SERVICE_ACCOUNT_KEY_PATH)
