#!/usr/bin/env python
#
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.api_core.exceptions import GoogleAPICallError, NotFound, RetryError
from google.cloud import securitycentermanagement_v1
from google.protobuf.field_mask_pb2 import FieldMask


# [START securitycenter_get_security_center_service]
def get_security_center_service(parent: str, service: str):
    """
    Gets service settings for the specified Security Command Center service.
    Args:
        parent: Use any one of the following options:
                - organizations/{organization_id}/locations/{location_id}
                - folders/{folder_id}/locations/{location_id}
                - projects/{project_id}/locations/{location_id}
        service: Valid value of the service
            For the full list of valid service values, see
            https://cloud.google.com/security-command-center/docs/reference/security-center-management/rest/v1/organizations.locations.securityCenterServices/get#path-parameters
    Returns:
        The retrieved service setting for the specified Security Command Center service.
    Raises:
        NotFound: If the specified Security Command Center service does not exist.
    """

    try:
        client = securitycentermanagement_v1.SecurityCenterManagementClient()

        request = securitycentermanagement_v1.GetSecurityCenterServiceRequest(
            name=f"{parent}/securityCenterServices/{service}",
        )

        response = client.get_security_center_service(request=request)
        print(f"Retrieved SecurityCenterService Setting for : {response.name}")
        return response
    except NotFound as e:
        print(f"SecurityCenterService not found: {e.message}")
        raise e
# [END securitycenter_get_security_center_service]


# [START securitycenter_list_security_center_service]
def list_security_center_service(parent: str):
    """
    Returns a list of all Security Command Center services for the given parent.

    Args:
        parent: Use any one of the following options:
                - organizations/{organization_id}/locations/{location_id}
                - folders/{folder_id}/locations/{location_id}
                - projects/{project_id}/locations/{location_id}
    Returns:
        List of retrieved all Security Command Center services.
    Raises:
        Exception: If an unexpected error occurs.
    """

    try:
        client = securitycentermanagement_v1.SecurityCenterManagementClient()

        request = securitycentermanagement_v1.ListSecurityCenterServicesRequest(
            parent=parent,
        )

        services = []
        # List all Security Command Center services present in the resource.
        for response in client.list_security_center_services(request=request):
            print(f"Security Center Service Name: {response.name}")
            services.append(response)
        return services

    except GoogleAPICallError as api_error:
        print(f"API call failed: {api_error}")
    except RetryError as retry_error:
        print(f"Retry error occurred: {retry_error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# [END securitycenter_list_security_center_service]


# [START securitycenter_update_security_center_service]
def update_security_center_service(parent: str, service: str):
    """
    Updates a Security Command Center service using the given update mask.

    Args:
        parent: Use any one of the following options:
                - organizations/{organization_id}/locations/{location_id}
                - folders/{folder_id}/locations/{location_id}
                - projects/{project_id}/locations/{location_id}
    Returns:
        The update service setting for the specified Security Command Center service.
    """

    try:
        client = securitycentermanagement_v1.SecurityCenterManagementClient()

        service = securitycentermanagement_v1.types.SecurityCenterService(
            name=f"{parent}/securityCenterServices/{service}",
            intended_enablement_state=securitycentermanagement_v1.types.SecurityCenterService.EnablementState.DISABLED,
        )

        # Create the request
        request = securitycentermanagement_v1.UpdateSecurityCenterServiceRequest(
            security_center_service=service,
            update_mask=FieldMask(paths=["intended_enablement_state"]),
        )

        # Make the API call
        updated_service = client.update_security_center_service(request=request)

        print(f"Updated SecurityCenterService: {updated_service.name} with new enablement state: {service.intended_enablement_state.name}")
        return updated_service

    except GoogleAPICallError as api_error:
        print(f"API call failed: {api_error}")
    except RetryError as retry_error:
        print(f"Retry error occurred: {retry_error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# [END securitycenter_update_security_center_service]
