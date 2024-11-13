# Copyright 2018 Google LLC
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

# [START healthcare_create_resource_from_file]
# Imports the types Dict and Any for runtime type hints.
from typing import Any, Dict  # noqa: E402


# [END healthcare_create_resource_from_file]
# [START healthcare_create_resource_from_file]
def create_resource_from_file(
    project_id: str,
    location: str,
    dataset_id: str,
    fhir_store_id: str,
    resource_type: str,
    resource_file: str,
) -> Dict[str, Any]:
    """Creates a new FHIR resource in a FHIR store from a JSON resource file.

    See
    https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample.
    See
    https://googleapis.github.io/google-api-python-client/docs/dyn/healthcare_v1.projects.locations.datasets.fhirStores.fhir.html#create
    for the Python API reference.

    Args:
      project_id: The project ID or project number of the Cloud project you want
        to use.
      location: The name of the parent dataset's location.
      dataset_id: The name of the parent dataset.
      fhir_store_id: The name of the FHIR store.
      resource_type: A valid FHIR resource type. See
        https://www.hl7.org/fhir/resourcelist.html.
      resource_file: The path to a JSON file containing a FHIR resource.

    Returns:
      A dict representing the created FHIR resource.
    """
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"

    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'
    # location = 'us-central1'
    # dataset_id = 'my-dataset'
    # fhir_store_id = 'my-fhir-store'
    fhir_store_parent = (
        f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
    )
    fhir_store_name = f"{fhir_store_parent}/fhirStores/{fhir_store_id}"

    # Load the local FHIR resource JSON file.
    with open(resource_file) as resource:
        resource_body = json.load(resource)

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .create(parent=fhir_store_name, type=resource_type, body=resource_body)
    )
    # Sets required application/fhir+json header on the googleapiclient.http.HttpRequest.
    request.headers["content-type"] = "application/fhir+json;charset=utf-8"
    response = request.execute()
    print(f"Created {resource_type} resource with ID {response['id']}")

    return response


# [END healthcare_create_resource_from_file]


# [START healthcare_create_resource]
# Imports the types Dict and Any for runtime type hints.
from typing import Any, Dict  # noqa: E402


# [END healthcare_create_resource]
# [START healthcare_create_resource]
def create_patient(
    project_id: str,
    location: str,
    dataset_id: str,
    fhir_store_id: str,
) -> Dict[str, Any]:
    """Creates a new Patient resource in a FHIR store.

    See
    https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample.
    See
    https://googleapis.github.io/google-api-python-client/docs/dyn/healthcare_v1.projects.locations.datasets.fhirStores.fhir.html#create
    for the Python API reference.

    Args:
      project_id: The project ID or project number of the Cloud project you want
        to use.
      location: The name of the parent dataset's location.
      dataset_id: The name of the parent dataset.
      fhir_store_id: The name of the FHIR store that holds the Patient resource.

    Returns:
      A dict representing the created Patient resource.
    """
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"

    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'
    # location = 'us-central1'
    # dataset_id = 'my-dataset'
    # fhir_store_id = 'my-fhir-store'
    fhir_store_parent = (
        f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
    )
    fhir_store_name = f"{fhir_store_parent}/fhirStores/{fhir_store_id}"

    patient_body = {
        "name": [{"use": "official", "family": "Smith", "given": ["Darcy"]}],
        "gender": "female",
        "birthDate": "1970-01-01",
        "resourceType": "Patient",
    }

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .create(parent=fhir_store_name, type="Patient", body=patient_body)
    )
    # Sets required application/fhir+json header on the googleapiclient.http.HttpRequest.
    request.headers["content-type"] = "application/fhir+json;charset=utf-8"
    response = request.execute()

    print(f"Created Patient resource with ID {response['id']}")
    return response


# [END healthcare_create_resource]


# [START healthcare_create_encounter]
# Imports the types Dict and Any for runtime type hints.
from typing import Any, Dict  # noqa: E402

# [END healthcare_create_encounter]


# [START healthcare_create_encounter]
def create_encounter(
    project_id: str,
    location: str,
    dataset_id: str,
    fhir_store_id: str,
    patient_id: str,
) -> Dict[str, Any]:
    """Creates a new Encounter resource in a FHIR store that references a Patient resource.

    See
    https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample.
    See
    https://googleapis.github.io/google-api-python-client/docs/dyn/healthcare_v1.projects.locations.datasets.fhirStores.fhir.html#create
    for the Python API reference.

    Args:
      project_id: The project ID or project number of the Cloud project you want
        to use.
      location: The name of the parent dataset's location.
      dataset_id: The name of the parent dataset.
      fhir_store_id: The name of the FHIR store.
      patient_id: The "logical id" of the referenced Patient resource. The ID is
        assigned by the server.

    Returns:
      A dict representing the created Encounter resource.
    """
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"

    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'
    # location = 'us-central1'
    # dataset_id = 'my-dataset'
    # fhir_store_id = 'my-fhir-store'
    # patient_id = 'b682d-0e-4843-a4a9-78c9ac64'  # replace with the associated Patient resource's ID
    fhir_store_parent = (
        f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
    )
    fhir_store_name = f"{fhir_store_parent}/fhirStores/{fhir_store_id}"

    encounter_body = {
        "status": "finished",
        "class": {
            "system": "http://hl7.org/fhir/v3/ActCode",
            "code": "IMP",
            "display": "inpatient encounter",
        },
        "reason": [
            {
                "text": (
                    "The patient had an abnormal heart rate. She was"
                    " concerned about this."
                )
            }
        ],
        "subject": {"reference": f"Patient/{patient_id}"},
        "resourceType": "Encounter",
    }

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .create(parent=fhir_store_name, type="Encounter", body=encounter_body)
    )
    # Sets required application/fhir+json header on the googleapiclient.http.HttpRequest.
    request.headers["content-type"] = "application/fhir+json;charset=utf-8"
    response = request.execute()
    print(f"Created Encounter resource with ID {response['id']}")

    return response


# [END healthcare_create_encounter]


# [START healthcare_create_observation]
# Imports the types Dict and Any for runtime type hints.
from typing import Any, Dict  # noqa: E402

# [END healthcare_create_observation]


# [START healthcare_create_observation]
def create_observation(
    project_id: str,
    location: str,
    dataset_id: str,
    fhir_store_id: str,
    patient_id: str,
    encounter_id: str,
) -> Dict[str, Any]:
    """Creates a new Observation resource in a FHIR store that references an Encounter and Patient resource.

    See
    https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample.
    See
    https://googleapis.github.io/google-api-python-client/docs/dyn/healthcare_v1.projects.locations.datasets.fhirStores.fhir.html#create
    for the Python API reference.

    Args:
      project_id: The project ID or project number of the Cloud project you want
        to use.
      location: The name of the parent dataset's location.
      dataset_id: The name of the parent dataset.
      fhir_store_id: The name of the FHIR store.
      patient_id: The "logical id" of the referenced Patient resource. The ID is
        assigned by the server.
      encounter_id: The "logical id" of the referenced Encounter resource. The ID
        is assigned by the server.

    Returns:
      A dict representing the created Observation resource.
    """
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"

    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'
    # location = 'us-central1'
    # dataset_id = 'my-dataset'
    # fhir_store_id = 'my-fhir-store'
    # patient_id = 'b682d-0e-4843-a4a9-78c9ac64'  # replace with the associated Patient resource's ID
    # encounter_id = 'a7602f-ffba-470a-a5c1-103f993c6  # replace with the associated Encounter resource's ID
    fhir_store_parent = (
        f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
    )
    fhir_observation_path = (
        f"{fhir_store_parent}/fhirStores/{fhir_store_id}/fhir/Observation"
    )

    observation_body = {
        "resourceType": "Observation",
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "8867-4",
                    "display": "Heart rate",
                }
            ]
        },
        "status": "final",
        "subject": {"reference": f"Patient/{patient_id}"},
        "effectiveDateTime": "2019-01-01T00:00:00+00:00",
        "valueQuantity": {"value": 80, "unit": "bpm"},
        "context": {"reference": f"Encounter/{encounter_id}"},
    }

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .create(
            parent=fhir_observation_path,
            type="Observation",
            body=observation_body,
        )
    )
    # Sets required application/fhir+json header on the googleapiclient.http.HttpRequest.
    request.headers["content-type"] = "application/fhir+json;charset=utf-8"
    response = request.execute()
    print(f"Created Observation resource with ID {response['id']}")

    return response


# [END healthcare_create_observation]


# [START healthcare_delete_resource]
def delete_resource(
    project_id: str,
    location: str,
    dataset_id: str,
    fhir_store_id: str,
    resource_type: str,
    resource_id: str,
) -> dict:
    """Deletes a FHIR resource.

    Regardless of whether the operation succeeds or
    fails, the server returns a 200 OK HTTP status code. To check that the
    resource was successfully deleted, search for or get the resource and
    see if it exists.

    See
    https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample.
    See
    https://googleapis.github.io/google-api-python-client/docs/dyn/healthcare_v1.projects.locations.datasets.fhirStores.fhir.html#delete
    for the Python API reference.
    Args:
      project_id: The project ID or project number of the Cloud project you want
        to use.
      location: The name of the parent dataset's location.
      dataset_id: The name of the parent dataset.
      fhir_store_id: The name of the FHIR store.
      resource_type: The type of the FHIR resource.
      resource_id: The "logical id" of the FHIR resource you want to delete. The
        ID is assigned by the server.

    Returns:
      An empty dict.
    """
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"

    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'
    # location = 'us-central1'
    # dataset_id = 'my-dataset'
    # fhir_store_id = 'my-fhir-store'
    # resource_type = 'Patient'
    # resource_id = 'b682d-0e-4843-a4a9-78c9ac64'
    fhir_store_parent = (
        f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
    )
    fhir_resource_path = f"{fhir_store_parent}/fhirStores/{fhir_store_id}/fhir/{resource_type}/{resource_id}"

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .delete(name=fhir_resource_path)
    )
    response = request.execute()
    print(f"Deleted {resource_type} resource with ID {resource_id}.")

    return response


# [END healthcare_delete_resource]


# [START healthcare_get_resource]
# Imports the types Dict and Any for runtime type hints.
from typing import Any, Dict  # noqa: E402


# [END healthcare_get_resource]
# [START healthcare_get_resource]
def get_resource(
    project_id: str,
    location: str,
    dataset_id: str,
    fhir_store_id: str,
    resource_type: str,
    resource_id: str,
) -> Dict[str, Any]:
    """Gets the contents of a FHIR resource.

    See
    https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample.
    See
    https://googleapis.github.io/google-api-python-client/docs/dyn/healthcare_v1.projects.locations.datasets.fhirStores.fhir.html#read
    for the Python API reference.

    Args:
      project_id: The project ID or project number of the Cloud project you want
        to use.
      location: The name of the parent dataset's location.
      dataset_id: The name of the parent dataset.
      fhir_store_id: The name of the FHIR store.
      resource_type: The type of FHIR resource.
      resource_id: The "logical id" of the resource you want to get the contents
        of. The ID is assigned by the server.

    Returns:
      A dict representing the FHIR resource.
    """
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"

    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'
    # location = 'us-central1'
    # dataset_id = 'my-dataset'
    # fhir_store_id = 'my-fhir-store'
    # resource_type = 'Patient'
    # resource_id = 'b682d-0e-4843-a4a9-78c9ac64'
    fhir_store_parent = (
        f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
    )
    fhir_resource_path = f"{fhir_store_parent}/fhirStores/{fhir_store_id}/fhir/{resource_type}/{resource_id}"

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .read(name=fhir_resource_path)
    )
    response = request.execute()
    print(
        f"Got contents of {resource_type} resource with ID {resource_id}:\n",
        json.dumps(response, indent=2),
    )

    return response


# [END healthcare_get_resource]


# [START healthcare_list_resource_history]
# Imports the types Dict and Any for runtime type hints.
from typing import Any, Dict  # noqa: E402


# [END healthcare_list_resource_history]
# [START healthcare_list_resource_history]
def list_resource_history(
    project_id: str,
    location: str,
    dataset_id: str,
    fhir_store_id: str,
    resource_type: str,
    resource_id: str,
) -> Dict[str, Any]:
    """Gets the history of a resource.

    See
    https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample.
    See
    https://googleapis.github.io/google-api-python-client/docs/dyn/healthcare_v1.projects.locations.datasets.fhirStores.fhir.html#history
    for the Python API reference.

    Args:
      project_id: The project ID or project number of the Cloud project you want
        to use.
      location: The name of the parent dataset's location.
      dataset_id: The name of the parent dataset.
      fhir_store_id: The name of the FHIR store.
      resource_type: The type of FHIR resource.
      resource_id: The "logical id" of the resource whose history you want to
        list. The ID is assigned by the server.

    Returns:
      A dict representing the FHIR resource.
    """
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"

    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'
    # location = 'us-central1'
    # dataset_id = 'my-dataset'
    # fhir_store_id = 'my-fhir-store'
    # resource_type = 'Patient'
    # resource_id = 'b682d-0e-4843-a4a9-78c9ac64'
    fhir_store_parent = (
        f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
    )
    fhir_resource_path = f"{fhir_store_parent}/fhirStores/{fhir_store_id}/fhir/{resource_type}/{resource_id}"

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .history(name=fhir_resource_path)
    )
    response = request.execute()
    print(
        f"History for {resource_type} resource with ID {resource_id}:\n"
        f" {json.dumps(response, indent=2)}"
    )
    return response


# [END healthcare_list_resource_history]


# [START healthcare_get_resource_history]
# Imports the types Dict and Any for runtime type hints.
from typing import Any, Dict  # noqa: E402


# [END healthcare_get_resource_history]
# [START healthcare_get_resource_history]
def get_resource_history(
    project_id: str,
    location: str,
    dataset_id: str,
    fhir_store_id: str,
    resource_type: str,
    resource_id: str,
    version_id: str,
) -> Dict[str, Any]:
    """Gets the contents of a version (current or historical) of a FHIR resource by version ID.

    See
    https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample.
    See
    https://googleapis.github.io/google-api-python-client/docs/dyn/healthcare_v1.projects.locations.datasets.fhirStores.fhir.html#vread
    for the Python API reference.

    Args:
      project_id: The project ID or project number of the Cloud project you want
        to use.
      location: The name of the parent dataset's location.
      dataset_id: The name of the parent dataset.
      fhir_store_id: The name of the FHIR store.
      resource_type: The type of FHIR resource.
      resource_id: The "logical id" of the resource whose details you want to view
        at a particular version. The ID is assigned by the server.
      version_id: The ID of the version. Changes whenever the FHIR resource is
        modified.

    Returns:
      A dict representing the FHIR resource at the specified version.
    """
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"

    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'
    # location = 'us-central1'
    # dataset_id = 'my-dataset'
    # fhir_store_id = 'my-fhir-store'
    # resource_type = 'Patient'
    # resource_id = 'b682d-0e-4843-a4a9-78c9ac64'
    # version_id = 'MTY4NDQ1MDc3MDU2ODgyNzAwMA'
    fhir_store_parent = (
        f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
    )
    fhir_resource_path = f"{fhir_store_parent}/fhirStores/{fhir_store_id}/fhir/{resource_type}/{resource_id}/_history/{version_id}"

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .vread(name=fhir_resource_path)
    )
    response = request.execute()
    print(
        f"Got contents of {resource_type} resource with ID {resource_id} at"
        f" version {version_id}:\n {json.dumps(response, indent=2)}"
    )

    return response


# [END healthcare_get_resource_history]


# [START healthcare_delete_resource_purge]
def delete_resource_purge(
    project_id: str,
    location: str,
    dataset_id: str,
    fhir_store_id: str,
    resource_type: str,
    resource_id: str,
) -> dict:
    """Deletes all versions of a FHIR resource (excluding the current version).

    See
    https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample.
    See
    https://googleapis.github.io/google-api-python-client/docs/dyn/healthcare_v1.projects.locations.datasets.fhirStores.fhir.html#Resource_purge
    for the Python API reference.

    Args:
      project_id: The project ID or project number of the Cloud project you want
        to use.
      location: The name of the parent dataset's location.
      dataset_id: The name of the parent dataset.
      fhir_store_id: The name of the FHIR store.
      resource_type: The type of the FHIR resource.
      resource_id: The "logical id" of the resource. The ID is assigned by the
        server.

    Returns:
      An empty dict.
    """
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"

    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'
    # location = 'us-central1'
    # dataset_id = 'my-dataset'
    # fhir_store_id = 'my-fhir-store'
    # resource_type = 'Patient'
    # resource_id = 'b682d-0e-4843-a4a9-78c9ac64'
    fhir_store_parent = (
        f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
    )
    fhir_resource_path = f"{fhir_store_parent}/fhirStores/{fhir_store_id}/fhir/{resource_type}/{resource_id}"

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .Resource_purge(name=fhir_resource_path)
    )
    response = request.execute()
    print(
        f"Deleted all versions of {resource_type} resource with ID"
        f" {resource_id} (excluding current version)."
    )
    return response


# [END healthcare_delete_resource_purge]


# [START healthcare_update_resource]
# Imports the types Dict and Any for runtime type hints.
from typing import Any, Dict  # noqa: E402


# [END healthcare_update_resource]
# [START healthcare_update_resource]
def update_resource(
    project_id: str,
    location: str,
    dataset_id: str,
    fhir_store_id: str,
    resource_type: str,
    resource_id: str,
) -> Dict[str, Any]:
    """Updates the entire contents of a FHIR resource.

    Creates a new current version if the resource already exists, or creates
    a new resource with an initial version if no resource already exists with
    the provided ID.

    See
    https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample.
    See
    https://googleapis.github.io/google-api-python-client/docs/dyn/healthcare_v1.projects.locations.datasets.fhirStores.fhir.html#update
    for the Python API reference.

    Args:
      project_id: The project ID or project number of the Cloud project you want
        to use.
      location: The name of the parent dataset's location.
      dataset_id: The name of the parent dataset.
      fhir_store_id: The name of the FHIR store.
      resource_type: The type of the FHIR resource.
      resource_id: The "logical id" of the resource. The ID is assigned by the
        server.

    Returns:
      A dict representing the updated FHIR resource.
    """
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"

    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'
    # location = 'us-central1'
    # dataset_id = 'my-dataset'
    # fhir_store_id = 'my-fhir-store'
    # resource_type = 'Patient'
    # resource_id = 'b682d-0e-4843-a4a9-78c9ac64'
    fhir_store_parent = (
        f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
    )
    fhir_resource_path = f"{fhir_store_parent}/fhirStores/{fhir_store_id}/fhir/{resource_type}/{resource_id}"

    # The following sample body works with a Patient resource and isn't guaranteed
    # to work with other types of FHIR resources. If necessary,
    # supply a new body with data that corresponds to the resource you
    # are updating.
    patient_body = {
        "resourceType": resource_type,
        "active": True,
        "id": resource_id,
    }

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .update(name=fhir_resource_path, body=patient_body)
    )
    # Sets required application/fhir+json header on the googleapiclient.http.HttpRequest.
    request.headers["content-type"] = "application/fhir+json;charset=utf-8"
    response = request.execute()

    print(
        f"Updated {resource_type} resource with ID {resource_id}:\n"
        f" {json.dumps(response, indent=2)}"
    )

    return response


# [END healthcare_update_resource]


# [START healthcare_patch_resource]
# Imports the types Dict and Any for runtime type hints.
from typing import Any, Dict  # noqa: E402


# [END healthcare_patch_resource]
# [START healthcare_patch_resource]
def patch_resource(
    project_id: str,
    location: str,
    dataset_id: str,
    fhir_store_id: str,
    resource_type: str,
    resource_id: str,
) -> Dict[str, Any]:
    """Updates part of an existing FHIR resource by applying the operations specified in a [JSON Patch](http://jsonpatch.com/) document.

    See
    https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample.
    See
    https://googleapis.github.io/google-api-python-client/docs/dyn/healthcare_v1.projects.locations.datasets.fhirStores.fhir.html#patch
    for the Python API reference.

    Args:
      project_id: The project ID or project number of the Cloud project you want
        to use.
      location: The name of the parent dataset's location.
      dataset_id: The name of the parent dataset.
      fhir_store_id: The name of the FHIR store.
      resource_type: The type of the FHIR resource.
      resource_id: The "logical id" of the resource. The ID is assigned by the
        server.

    Returns:
      A dict representing the patched FHIR resource.
    """
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"

    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'
    # location = 'us-central1'
    # dataset_id = 'my-dataset'
    # fhir_store_id = 'my-fhir-store'
    # resource_type = 'Patient'
    # resource_id = 'b682d-0e-4843-a4a9-78c9ac64'
    fhir_store_parent = (
        f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
    )
    fhir_resource_path = f"{fhir_store_parent}/fhirStores/{fhir_store_id}/fhir/{resource_type}/{resource_id}"

    # The following sample body works with a Patient resource and isn't guaranteed
    # to work with other types of FHIR resources. If necessary,
    # supply a new body with data that corresponds to the resource you
    # are updating.
    patient_body = [{"op": "replace", "path": "/active", "value": False}]

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .patch(name=fhir_resource_path, body=patient_body)
    )

    # Sets required application/json-patch+json header.
    # See https://tools.ietf.org/html/rfc6902 for more information.
    request.headers["content-type"] = "application/json-patch+json"

    response = request.execute()

    print(
        f"Patched {resource_type} resource with ID {resource_id}:\n"
        f" {json.dumps(response, indent=2)}"
    )

    return response


# [END healthcare_patch_resource]


# [START healthcare_search_resources_get]
def search_resources_get(
    project_id,
    location,
    dataset_id,
    fhir_store_id,
    resource_type,
):
    """
    Uses the searchResources GET method to search for resources in the given FHIR store.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample."""
    # Imports Python's built-in "os" module
    import os

    # Imports the google.auth.transport.requests transport
    from google.auth.transport import requests

    # Imports a module to allow authentication using a service account
    from google.oauth2 import service_account

    # Gets credentials from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    # Creates a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    # URL to the Cloud Healthcare API endpoint and version
    base_url = "https://healthcare.googleapis.com/v1"

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the parent dataset's ID
    # fhir_store_id = 'my-fhir-store' # replace with the FHIR store ID
    # resource_type = 'Patient'  # replace with the FHIR resource type
    url = f"{base_url}/projects/{project_id}/locations/{location}"

    resource_path = "{}/datasets/{}/fhirStores/{}/fhir/{}".format(
        url, dataset_id, fhir_store_id, resource_type
    )

    response = session.get(resource_path)
    response.raise_for_status()

    resources = response.json()

    print(
        "Using GET request, found a total of {} {} resources:".format(
            resources["total"], resource_type
        )
    )
    print(json.dumps(resources, indent=2))

    return resources


# [END healthcare_search_resources_get]


# [START healthcare_search_resources_post]
def search_resources_post(project_id, location, dataset_id, fhir_store_id):
    """
    Searches for resources in the given FHIR store. Uses the
    _search POST method and a query string containing the
    information to search for. In this sample, the search criteria is
    'family:exact=Smith' on a Patient resource.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample."""
    # Imports Python's built-in "os" module
    import os

    # Imports the google.auth.transport.requests transport
    from google.auth.transport import requests

    # Imports a module to allow authentication using a service account
    from google.oauth2 import service_account

    # Gets credentials from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    # Creates a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    # URL to the Cloud Healthcare API endpoint and version
    base_url = "https://healthcare.googleapis.com/v1"

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the parent dataset's ID
    # fhir_store_id = 'my-fhir-store' # replace with the FHIR store ID
    url = f"{base_url}/projects/{project_id}/locations/{location}"

    fhir_store_path = "{}/datasets/{}/fhirStores/{}/fhir".format(
        url, dataset_id, fhir_store_id
    )

    resource_path = f"{fhir_store_path}/Patient/_search?family:exact=Smith"

    # Sets required application/fhir+json header on the request
    headers = {"Content-Type": "application/fhir+json;charset=utf-8"}

    response = session.post(resource_path, headers=headers)
    response.raise_for_status()

    resources = response.json()
    print(
        "Using POST request, found a total of {} Patient resources:".format(
            resources["total"]
        )
    )

    print(json.dumps(resources, indent=2))

    return resources


# [END healthcare_search_resources_post]


# [START healthcare_get_patient_everything]
def get_patient_everything(
    project_id,
    location,
    dataset_id,
    fhir_store_id,
    resource_id,
):
    """Gets all the resources in the patient compartment.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample."""
    # Imports Python's built-in "os" module
    import os

    # Imports the google.auth.transport.requests transport
    from google.auth.transport import requests

    # Imports a module to allow authentication using a service account
    from google.oauth2 import service_account

    # Gets credentials from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    # Creates a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    # URL to the Cloud Healthcare API endpoint and version
    base_url = "https://healthcare.googleapis.com/v1"

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the parent dataset's ID
    # fhir_store_id = 'my-fhir-store' # replace with the FHIR store ID
    # resource_id = 'b682d-0e-4843-a4a9-78c9ac64'  # replace with the Patient resource's ID
    url = f"{base_url}/projects/{project_id}/locations/{location}"

    resource_path = "{}/datasets/{}/fhirStores/{}/fhir/{}/{}".format(
        url, dataset_id, fhir_store_id, "Patient", resource_id
    )
    resource_path += "/$everything"

    # Sets required application/fhir+json header on the request
    headers = {"Content-Type": "application/fhir+json;charset=utf-8"}

    response = session.get(resource_path, headers=headers)
    response.raise_for_status()

    resource = response.json()

    print(json.dumps(resource, indent=2))

    return resource


# [END healthcare_get_patient_everything]


# [START healthcare_fhir_execute_bundle]
def execute_bundle(
    project_id,
    location,
    dataset_id,
    fhir_store_id,
    bundle,
):
    """Executes the operations in the given bundle.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample."""
    # Imports Python's built-in "os" module
    import os

    # Imports the google.auth.transport.requests transport
    from google.auth.transport import requests

    # Imports a module to allow authentication using a service account
    from google.oauth2 import service_account

    # Gets credentials from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    # Creates a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    # URL to the Cloud Healthcare API endpoint and version
    base_url = "https://healthcare.googleapis.com/v1"

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the parent dataset's ID
    # fhir_store_id = 'my-fhir-store' # replace with the FHIR store ID
    # bundle = 'bundle.json'  # replace with the bundle file
    url = f"{base_url}/projects/{project_id}/locations/{location}"

    resource_path = "{}/datasets/{}/fhirStores/{}/fhir".format(
        url, dataset_id, fhir_store_id
    )

    headers = {"Content-Type": "application/fhir+json;charset=utf-8"}

    with open(bundle) as bundle_file:
        bundle_file_content = bundle_file.read()

    response = session.post(resource_path, headers=headers, data=bundle_file_content)
    response.raise_for_status()

    resource = response.json()

    print(f"Executed bundle from file: {bundle}")
    print(json.dumps(resource, indent=2))

    return resource


# [END healthcare_fhir_execute_bundle]


# [START healthcare_create_implementation_guide]
def create_implementation_guide(
    project_id, location, dataset_id, fhir_store_id, implementation_guide_file
):
    """
    Creates a new ImplementationGuide resource in a FHIR store from an
    ImplementationGuide JSON file.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample."""
    # Imports Python's built-in "os" module
    import os

    # Imports the google.auth.transport.requests transport
    from google.auth.transport import requests

    # Imports a module to allow authentication using a service account
    from google.oauth2 import service_account

    # Gets credentials from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    # Creates a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    # URL to the Cloud Healthcare API endpoint and version
    base_url = "https://healthcare.googleapis.com/v1"

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the parent dataset's ID
    # fhir_store_id = 'my-fhir-store' # replace with the FHIR store ID
    # implementation_guide_definition_file = 'ImplementationGuide-hl7.fhir.us.core.json'  # replace with the ImplementationGuide resource file
    url = f"{base_url}/projects/{project_id}/locations/{location}"

    fhir_store_path = "{}/datasets/{}/fhirStores/{}/fhir/ImplementationGuide".format(
        url, dataset_id, fhir_store_id
    )

    # Sets required application/fhir+json header on the request
    headers = {"Content-Type": "application/fhir+json;charset=utf-8"}

    with open(implementation_guide_file) as implementation_guide:
        implementation_guide_content = json.load(implementation_guide)

    response = session.post(
        fhir_store_path, headers=headers, json=implementation_guide_content
    )
    response.raise_for_status()

    resource = response.json()

    print("Created ImplementationGuide resource with ID {}".format(resource["id"]))

    return response


# [END healthcare_create_implementation_guide]


# [START healthcare_enable_implementation_guide]
def enable_implementation_guide(
    project_id,
    location,
    dataset_id,
    fhir_store_id,
    implementation_guide_url,
):
    """
    Patches an existing FHIR store to enable an ImplementationGuide resource
    that exists in the FHIR store.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample."""
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"
    # Instantiates an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the dataset's location
    # dataset_id = 'my-dataset'  # replace with your dataset ID
    # fhir_store_id = 'my-fhir-store'  # replace with the FHIR store's ID
    # implementation_guide_url =
    # 'http://hl7.org/fhir/us/core/ImplementationGuide/hl7.fhir.us.core'  #
    # replace with the 'url' property in the ImplementationGuide resource
    fhir_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    fhir_store_name = f"{fhir_store_parent}/fhirStores/{fhir_store_id}"

    validation_config = {
        "validationConfig": {"enabledImplementationGuides": [implementation_guide_url]}
    }

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .patch(
            name=fhir_store_name, updateMask="validationConfig", body=validation_config
        )
    )

    response = request.execute()
    print(
        "Enabled ImplementationGuide with URL {} on FHIR store {}".format(
            implementation_guide_url, fhir_store_id
        )
    )

    return response


# [END healthcare_enable_implementation_guide]


# [START healthcare_create_structure_definition]
def create_structure_definition(
    project_id, location, dataset_id, fhir_store_id, structure_definition_file
):
    """
    Creates a new StructureDefinition resource in a FHIR store from a
    StructureDefinition JSON file.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample."""
    # Imports Python's built-in "os" module
    import os

    # Imports the google.auth.transport.requests transport
    from google.auth.transport import requests

    # Imports a module to allow authentication using a service account
    from google.oauth2 import service_account

    # Gets credentials from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    # Creates a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    # URL to the Cloud Healthcare API endpoint and version
    base_url = "https://healthcare.googleapis.com/v1"

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the parent dataset's ID
    # fhir_store_id = 'my-fhir-store' # replace with the FHIR store ID
    # structure_definition_file = 'StructureDefinition-us-core-patient.json'  # replace with the StructureDefinition resource file
    url = f"{base_url}/projects/{project_id}/locations/{location}"

    fhir_store_path = "{}/datasets/{}/fhirStores/{}/fhir/StructureDefinition".format(
        url, dataset_id, fhir_store_id
    )

    # Sets required application/fhir+json header on the request
    headers = {"Content-Type": "application/fhir+json;charset=utf-8"}

    with open(structure_definition_file) as structure_definition:
        structure_definition_content = json.load(structure_definition)

    response = session.post(
        fhir_store_path, headers=headers, json=structure_definition_content
    )
    response.raise_for_status()

    resource = response.json()

    print("Created StructureDefinition resource with ID {}".format(resource["id"]))

    return response


# [END healthcare_create_structure_definition]


# [START healthcare_resource_validate]
def validate_resource(
    project_id,
    location,
    dataset_id,
    fhir_store_id,
    resource_type,
):
    """Validates an input FHIR resource's conformance to the base profile
    configured on the FHIR store.
    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample."""
    # Imports Python's built-in "os" module
    import os

    # Imports the google.auth.transport.requests transport
    from google.auth.transport import requests

    # Imports a module to allow authentication using a service account
    from google.oauth2 import service_account

    # Gets credentials from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    # Creates a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    # URL to the Cloud Healthcare API endpoint and version
    base_url = "https://healthcare.googleapis.com/v1"

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the parent dataset's ID
    # fhir_store_id = 'my-fhir-store' # replace with the FHIR store ID
    # resource_type = 'Patient'  # replace with the FHIR resource type
    url = f"{base_url}/projects/{project_id}/locations/{location}"

    resource_path = "{}/datasets/{}/fhirStores/{}/fhir/{}".format(
        url, dataset_id, fhir_store_id, resource_type
    )

    resource_path += "/$validate"

    # The body shown works with a Patient resource and is not guaranteed
    # to work with other types of FHIR resources. If necessary,
    # supply a new body with data that corresponds to the resource you
    # are validating.
    body = {
        "name": [{"use": "official", "family": "Smith", "given": ["Darcy"]}],
        "gender": "female",
        "birthDate": "1970-01-01",
        "resourceType": "Patient",
    }

    # Sets required application/fhir+json header on the request
    headers = {"Content-Type": "application/fhir+json;charset=utf-8"}

    response = session.post(resource_path, headers=headers, json=body)
    response.raise_for_status()

    resource = response.json()

    print(json.dumps(resource))

    return resource


# [END healthcare_resource_validate]


# [START healthcare_resource_validate_profile_url]
def validate_resource_profile_url(
    project_id, location, dataset_id, fhir_store_id, resource_type, profile_url
):
    """Validates an input FHIR resource's conformance to a profile URL. The
    profile StructureDefinition resource must exist in the FHIR store before
    performing validation against the URL.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample."""
    # Imports Python's built-in "os" module
    import os

    # Imports the google.auth.transport.requests transport
    from google.auth.transport import requests

    # Imports a module to allow authentication using a service account
    from google.oauth2 import service_account

    # Gets credentials from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    # Creates a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    # URL to the Cloud Healthcare API endpoint and version
    base_url = "https://healthcare.googleapis.com/v1"

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the parent dataset's ID
    # fhir_store_id = 'my-fhir-store' # replace with the FHIR store ID
    # resource_type = 'Patient'  # replace with the FHIR resource type
    # profile_url = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient'  # replace with the profile URL
    url = f"{base_url}/projects/{project_id}/locations/{location}"

    resource_path = "{}/datasets/{}/fhirStores/{}/fhir/{}".format(
        url, dataset_id, fhir_store_id, resource_type
    )

    resource_path += "/$validate"
    params = {"profile": profile_url}

    # The body shown works with a Patient resource and is not guaranteed
    # to work with other types of FHIR resources. If necessary,
    # supply a new body with data that corresponds to the resource you
    # are validating and supply a new resource_type.
    body = {
        "name": [{"use": "official", "family": "Smith", "given": ["Darcy"]}],
        "gender": "female",
        "birthDate": "1970-01-01",
        "resourceType": "Patient",
    }

    # Sets required application/fhir+json header on the request
    headers = {"Content-Type": "application/fhir+json;charset=utf-8"}

    response = session.post(resource_path, headers=headers, json=body, params=params)
    response.raise_for_status()

    resource = response.json()

    print(json.dumps(resource))

    return resource


# [END healthcare_resource_validate_profile_url]


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

    parser.add_argument("--fhir_store_id", default=None, help="Name of FHIR store")

    parser.add_argument(
        "--resource_file",
        default=None,
        help="A JSON file containing the contents of a FHIR resource to create",
    )

    parser.add_argument(
        "--resource_type",
        default=None,
        help="The type of resource. First letter must be capitalized",
    )

    parser.add_argument(
        "--resource_id", default=None, help="Identifier for a FHIR resource"
    )

    parser.add_argument(
        "--patient_id",
        default=None,
        help="Identifier for a Patient resource. Can be used as a reference "
        "for an Encounter/Observation",
    )

    parser.add_argument(
        "--encounter_id",
        default=None,
        help="Identifier for an Encounter resource. Can be used as a "
        "reference for an Observation",
    )

    parser.add_argument(
        "--bundle",
        default=None,
        help="Name of file containing bundle of operations to execute",
    )

    parser.add_argument(
        "--uri_prefix", default=None, help="Prefix of gs:// URIs for import and export"
    )

    parser.add_argument("--version_id", default=None, help="Version of a FHIR resource")

    parser.add_argument(
        "--structure_definition_file",
        default=None,
        help="A StructureDefinition resource JSON file",
    )

    parser.add_argument(
        "--profile_url",
        default=None,
        help="The canonical URL of the FHIR profile to validate against",
    )

    parser.add_argument(
        "--implementation_guide_file",
        default=None,
        help="An ImplementationGuide resource JSON file",
    )

    parser.add_argument(
        "--implementation_guide_url",
        default=None,
        help="the URL defined in the 'url' property of the ImplementationGuide resource",
    )

    command = parser.add_subparsers(dest="command")

    command.add_parser(
        "create-resource-from-file", help=create_resource_from_file.__doc__
    )
    command.add_parser("create-patient", help=create_patient.__doc__)
    command.add_parser("create-encounter", help=create_encounter.__doc__)
    command.add_parser("create-observation", help=create_observation.__doc__)
    command.add_parser("delete-resource", help=delete_resource.__doc__)
    command.add_parser("get-resource", help=get_resource.__doc__)
    command.add_parser("list-resource-history", help=list_resource_history.__doc__)
    command.add_parser("execute-bundle", help=execute_bundle.__doc__)
    command.add_parser("get-resource-history", help=get_resource_history.__doc__)
    command.add_parser("delete-resource-purge", help=delete_resource_purge.__doc__)
    command.add_parser("update-resource", help=update_resource.__doc__)
    command.add_parser("patch-resource", help=patch_resource.__doc__)
    command.add_parser("search-resources-get", help=search_resources_get.__doc__)
    command.add_parser("search-resources-post", help=search_resources_get.__doc__)
    command.add_parser("get-patient-everything", help=get_patient_everything.__doc__)
    command.add_parser(
        "create-structure-definition", help=create_structure_definition.__doc__
    )
    command.add_parser(
        "create-implementation-guide", help=create_implementation_guide.__doc__
    )
    command.add_parser(
        "enable-implementation-guide", help=enable_implementation_guide.__doc__
    )
    command.add_parser("validate-resource", help=validate_resource.__doc__)
    command.add_parser(
        "validate-resource-profile-url", help=validate_resource_profile_url.__doc__
    )

    return parser.parse_args()


# Comment noqa because otherwise flake8 returns "C901 'run_command' is too
# complex" error
def run_command(args):  # noqa
    """Calls the program using the specified command."""
    if args.project_id is None:
        print(
            "You must specify a project ID or set the "
            '"GOOGLE_CLOUD_PROJECT" environment variable.'
        )
        return

    elif args.command == "create-resource-from-file":
        create_resource_from_file(
            args.project_id,
            args.location,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type,
            args.resource_file,
        )

    elif args.command == "create-patient":
        create_patient(
            args.project_id,
            args.location,
            args.dataset_id,
            args.fhir_store_id,
        )

    elif args.command == "create-encounter":
        create_encounter(
            args.project_id,
            args.location,
            args.dataset_id,
            args.fhir_store_id,
            args.patient_id,
        )

    elif args.command == "create-observation":
        create_observation(
            args.project_id,
            args.location,
            args.dataset_id,
            args.fhir_store_id,
            args.patient_id,
            args.encounter_id,
        )

    elif args.command == "get-resource":
        get_resource(
            args.project_id,
            args.location,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type,
            args.resource_id,
        )

    elif args.command == "execute-bundle":
        execute_bundle(
            args.project_id,
            args.location,
            args.dataset_id,
            args.fhir_store_id,
            args.bundle,
        )

    elif args.command == "list-resource-history":
        list_resource_history(
            args.project_id,
            args.location,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type,
            args.resource_id,
        )

    elif args.command == "get-resource-history":
        get_resource_history(
            args.project_id,
            args.location,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type,
            args.resource_id,
            args.version_id,
        )

    elif args.command == "delete-resource-purge":
        delete_resource_purge(
            args.project_id,
            args.location,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type,
            args.resource_id,
        )

    elif args.command == "update-resource":
        update_resource(
            args.project_id,
            args.location,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type,
            args.resource_id,
        )

    elif args.command == "patch-resource":
        patch_resource(
            args.project_id,
            args.location,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type,
            args.resource_id,
        )

    elif args.command == "delete-resource":
        delete_resource(
            args.project_id,
            args.location,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type,
            args.resource_id,
        )

    elif args.command == "search-resources-get":
        search_resources_get(
            args.project_id,
            args.location,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type,
        )

    elif args.command == "search-resources-post":
        search_resources_post(
            args.project_id,
            args.location,
            args.dataset_id,
            args.fhir_store_id,
        )

    elif args.command == "get-patient-everything":
        get_patient_everything(
            args.project_id,
            args.location,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_id,
        )

    elif args.command == "create-implementation-guide":
        create_implementation_guide(
            args.project_id,
            args.location,
            args.dataset_id,
            args.fhir_store_id,
            args.implementation_guide_file,
        )

    elif args.command == "enable-implementation-guide":
        enable_implementation_guide(
            args.project_id,
            args.location,
            args.dataset_id,
            args.fhir_store_id,
            args.implementation_guide_url,
        )

    elif args.command == "create-structure-definition":
        create_structure_definition(
            args.project_id,
            args.location,
            args.dataset_id,
            args.fhir_store_id,
            args.structure_definition_file,
        )

    elif args.command == "validate-resource":
        validate_resource(
            args.project_id,
            args.location,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type,
        )

    elif args.command == "validate-resource-profile-url":
        validate_resource_profile_url(
            args.project_id,
            args.location,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type,
            args.profile_url,
        )


def main():
    args = parse_command_line_args()
    run_command(args)


if __name__ == "__main__":
    main()
