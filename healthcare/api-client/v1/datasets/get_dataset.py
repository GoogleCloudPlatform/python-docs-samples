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


# [START healthcare_get_dataset]
# Imports the Dict type for runtime type hints.
from typing import Dict


# [END healthcare_get_dataset]
# [START healthcare_get_dataset]
def get_dataset(project_id: str, location: str, dataset_id: str) -> Dict[str, str]:
    """Gets any metadata associated with a dataset.

    See
    https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/datasets
    before running the sample.
    See https://googleapis.github.io/google-api-python-client/docs/dyn/healthcare_v1.projects.locations.datasets.html#get
    for the Python API reference.

    Args:
      project_id: The project ID or project number of the Google Cloud project you want
          to use.
      location: The name of the dataset's location.
      dataset_id: The name of the dataset to get.

    Returns:
      A dictionary representing a Dataset resource.
    """
    # Imports HttpError from the Google Python API client errors module.
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery
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
    dataset_name = f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"

    request = client.projects().locations().datasets()

    try:
        dataset = request.get(name=dataset_name).execute()
        print(f"Name: {dataset.get('name')}")
        return dataset
    except HttpError as err:
        raise err


# [END healthcare_get_dataset]
