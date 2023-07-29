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

# [START healthcare_create_dataset]
# Imports the Dict type for runtime type hints.
from typing import Dict


# [END healthcare_create_dataset]
# [START healthcare_create_dataset]
def create_dataset(project_id: str, location: str, dataset_id: str) -> Dict[str, str]:
    """Creates a Cloud Healthcare API dataset.

    See
    https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/datasets
    before running the sample.
    See
    https://googleapis.github.io/google-api-python-client/docs/dyn/healthcare_v1.projects.locations.datasets.html#create
    for the Python API reference.

    Args:
      project_id: The project ID or project number of the Google Cloud project you want
          to use.
      location: The name of the dataset's location.
      dataset_id: The ID of the dataset to create.

    Returns:
      A dictionary representing a long-running operation that results from
      calling the 'CreateDataset' method. Dataset creation is typically fast.
    """
    # Imports the Python built-in time module.
    import time

    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    # Imports HttpError from the Google Python API client errors module.
    from googleapiclient.errors import HttpError

    api_version = "v1"
    service_name = "healthcare"
    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'
    # location = 'us-central1'
    # dataset_id = 'my-dataset'
    dataset_parent = f"projects/{project_id}/locations/{location}"

    request = (
        client.projects()
        .locations()
        .datasets()
        .create(parent=dataset_parent, body={}, datasetId=dataset_id)
    )

    # Wait for operation to complete.
    start_time = time.time()
    max_time = 600  # 10 minutes, but dataset creation is typically only a few seconds.

    try:
        operation = request.execute()
        while not operation.get("done", False):
            # Poll until the operation finishes.
            print("Waiting for operation to finish...")
            if time.time() - start_time > max_time:
                raise TimeoutError("Timed out waiting for operation to finish.")
            operation = (
                client.projects()
                .locations()
                .datasets()
                .operations()
                .get(name=operation["name"])
                .execute()
            )
            # Wait 5 seconds between each poll to the operation.
            time.sleep(5)

        if "error" in operation:
            raise RuntimeError(f"Create dataset operation failed: {operation['error']}")
        else:
            dataset_name = operation["response"]["name"]
            print(f"Created dataset: {dataset_name}")
            return operation

    except HttpError as err:
        # A common error is when the dataset already exists.
        if err.resp.status == 409:
            print(f"Dataset with ID {dataset_id} already exists.")
            return
        else:
            raise err


# [END healthcare_create_dataset]
