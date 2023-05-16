#!/usr/bin/env python

# Copyright 2020 Google Inc. All Rights Reserved.
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

from google.cloud import servicedirectory_v1
from google.cloud.servicedirectory_v1 import (
    Endpoint,
    Namespace,
    ResolveServiceResponse,
    Service,
)


# [START servicedirectory_create_namespace]
def create_namespace(project_id: str, location: str, namespace_id: str) -> Namespace:
    """Creates a namespace in the given location.

    Args:
        project_id: Your Google Cloud project id.
        location: The Google Cloud region containing the new namespace.
        namespace_id: A unique id for the namespace.

    Returns:
        The created namespace.
    """

    client = servicedirectory_v1.RegistrationServiceClient()

    namespace = servicedirectory_v1.Namespace(
        name=client.namespace_path(project_id, location, namespace_id)
    )

    response = client.create_namespace(
        parent=f"projects/{project_id}/locations/{location}",
        namespace=namespace,
        namespace_id=namespace_id,
    )

    print(f"Created namespace {response.name}.")

    return response


# [END servicedirectory_create_namespace]


# [START servicedirectory_delete_namespace]
def delete_namespace(project_id: str, location: str, namespace_id: str) -> None:
    """Deletes a namespace in the given location.

    Args:
        project_id: Your Google Cloud project id.
        location: The Google Cloud region containing the namespace to delete.
        namespace_id: The id for the namespace to delete.
    """

    client = servicedirectory_v1.RegistrationServiceClient()

    namespace_name = client.namespace_path(project_id, location, namespace_id)

    client.delete_namespace(name=namespace_name)

    print(f"Deleted namespace {namespace_name}.")


# [END servicedirectory_delete_namespace]


# [START servicedirectory_create_service]
def create_service(
    project_id: str, location: str, namespace_id: str, service_id: str
) -> Service:
    """Creates a service in the given namespace.

    Args:
        project_id: Your Google Cloud project id.
        location: The Google Cloud region containing the namespace.
        namespace_id: The id of the parent namespace.
        service_id: The id of the service you are creating. Service names must be unique within a namespace and follow
            conventions for DNS labels.

    Returns:
        The created service.
    """

    client = servicedirectory_v1.RegistrationServiceClient()

    service = servicedirectory_v1.Service(
        name=client.service_path(project_id, location, namespace_id, service_id)
    )

    response = client.create_service(
        parent=client.namespace_path(project_id, location, namespace_id),
        service=service,
        service_id=service_id,
    )

    print(f"Created service {response.name}.")

    return response


# [END servicedirectory_create_service]


# [START servicedirectory_delete_service]
def delete_service(
    project_id: str, location: str, namespace_id: str, service_id: str
) -> None:
    """Deletes a service in the given namespace.

    Args:
        project_id: Your Google Cloud project id.
        location: The Google Cloud region containing the namespace.
        namespace_id: The id of the parent namespace.
        service_id: The id of the service to delete.
    """

    client = servicedirectory_v1.RegistrationServiceClient()

    service_name = client.service_path(project_id, location, namespace_id, service_id)

    client.delete_service(name=service_name)

    print(f"Deleted service {service_name}.")


# [END servicedirectory_delete_service]


# [START servicedirectory_resolve_service]
def resolve_service(
    project_id: str, location: str, namespace_id: str, service_id: str
) -> ResolveServiceResponse:
    """Resolves a service in the given namespace.

    Args:
        project_id: Your Google Cloud project id.
        location: The Google Cloud region containing the namespace.
        namespace_id: The id of the parent namespace.
        service_id: The id of the service to resolve.

    Returns:
        The resolved service response, which returns all properties of the service, all endpoints, and all annotations.
    """

    client = servicedirectory_v1.LookupServiceClient()

    request = servicedirectory_v1.ResolveServiceRequest(
        name=servicedirectory_v1.RegistrationServiceClient().service_path(
            project_id, location, namespace_id, service_id
        )
    )

    response = client.resolve_service(request=request)

    print("Endpoints found:")
    for endpoint in response.service.endpoints:
        print(f"{endpoint.name} -- {endpoint.address}:{endpoint.port}")

    return response


# [END servicedirectory_resolve_service]


# [START servicedirectory_create_endpoint]
def create_endpoint(
    project_id: str,
    location: str,
    namespace_id: str,
    service_id: str,
    endpoint_id: str,
    address: str,
    port: str,
) -> Endpoint:
    """Creates a endpoint in the given service.

    An endpoint consists of a unique name, an optional IP address and a port, and key-value annotations.

    Args:
        project_id: Your Google Cloud project id.
        location: The Google Cloud region containing the namespace.
        namespace_id: The id of the parent namespace.
        service_id: The id of the parent service.
        endpoint_id: A name for the endpoint you are creating.
        address: IP address for the endpoint.
        port: Port number for the endpoint.

    Returns:
        The created endpoint.
    """

    client = servicedirectory_v1.RegistrationServiceClient()

    endpoint = servicedirectory_v1.Endpoint(
        name=client.endpoint_path(
            project_id, location, namespace_id, service_id, endpoint_id
        ),
        address=address,
        port=port,
    )

    response = client.create_endpoint(
        parent=client.service_path(project_id, location, namespace_id, service_id),
        endpoint=endpoint,
        endpoint_id=endpoint_id,
    )

    print(f"Created endpoint {response.name}.")

    return response


# [END servicedirectory_create_endpoint]


# [START servicedirectory_delete_endpoint]
def delete_endpoint(
    project_id: str,
    location: str,
    namespace_id: str,
    service_id: str,
    endpoint_id: str,
) -> None:
    """Deletes a endpoint in the given service.

    Args:
        project_id: Your Google Cloud project id.
        location: The Google Cloud region containing the namespace.
        namespace_id: The id of the parent namespace.
        service_id: The id of the parent service.
        endpoint_id: The id of the endpoint to delete.
    """

    client = servicedirectory_v1.RegistrationServiceClient()

    endpoint_name = client.endpoint_path(
        project_id, location, namespace_id, service_id, endpoint_id
    )

    client.delete_endpoint(name=endpoint_name)

    print(f"Deleted endpoint {endpoint_name}.")


# [END servicedirectory_delete_endpoint]
