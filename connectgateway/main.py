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

import sys
from google.auth.transport import requests
from google.cloud.gkeconnect import gateway_v1
from google.oauth2 import service_account
from kubernetes import client, config

# --- Configuration ---
# TODO(developer): Update the following lines.
SERVICE_ACCOUNT_KEY_PATH = 'SERVICE_ACCOUNT_KEY_PATH'
PROJECT_NUMBER = 'PROJECT_NUMBER'
MEMBERSHIP_LOCATION = 'LOCATION'
MEMBERSHIP_ID = 'MEMBERSHIP_ID'
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

def get_gateway_url() -> str:
    """Fetches the GKE Connect Gateway URL for the specified membership."""
    try:
        gateway_client = gateway_v1.GatewayControlClient()
        request = gateway_v1.GenerateCredentialsRequest()
        request.name = f'projects/{PROJECT_NUMBER}/locations/{MEMBERSHIP_LOCATION}/memberships/{MEMBERSHIP_ID}'
        response = gateway_client.generate_credentials(request=request)
        print(f'GKE Connect Gateway Endpoint: {response.endpoint}')
        return response.endpoint
    except Exception as e:
        print(f'Error fetching GKE Connect Gateway URL: {e}')
        sys.exit(1)

def configure_kubernetes_client(gateway_url: str) -> client.CoreV1Api:
    """Configures the Kubernetes client with the GKE Connect Gateway URL and credentials."""

    configuration = client.Configuration()

    # Configure the API client with the custom host.
    configuration.host = gateway_url

    # Set the authentication header with the GCP OAuth token
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_KEY_PATH, scopes=SCOPES
        )
    except FileNotFoundError:
        print(f"Error: Service account key file not found at {SERVICE_ACCOUNT_KEY_PATH}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading service account credentials: {e}")
        sys.exit(1)
    auth_req = requests.Request()
    credentials.refresh(auth_req)
    configuration.api_key = {'authorization': f'Bearer {credentials.token}'}

    api_client = client.ApiClient(configuration=configuration)
    return client.CoreV1Api(api_client)

def list_namespaces(api_client: client.CoreV1Api):
    """Lists all namespaces in the Kubernetes cluster."""
    try:
        namespace_list = api_client.list_namespace()
        if namespace_list.items:
            print("\n--- List of Namespaces ---")
            for namespace in namespace_list.items:
                print(f"Name: {namespace.metadata.name}")
        else:
            print("No namespaces found in the cluster.")
    except client.ApiException as e:
        print(f"Error listing namespaces: {e}\nStatus: {e.status}\nReason: {e.reason}")

def main():
    """Main function to connect to the cluster and list pods."""
    gateway_url = get_gateway_url()
    core_v1_api = configure_kubernetes_client(gateway_url)
    list_namespaces(core_v1_api)

if __name__ == "__main__":
    main()
