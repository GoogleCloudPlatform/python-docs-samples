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


# [START healthcare_dataset_get_iam_policy]
# Imports the Dict and Any types for runtime type hints.
from typing import Any, Dict


# [END healthcare_dataset_get_iam_policy]
# [START healthcare_dataset_get_iam_policy]
def get_dataset_iam_policy(
    project_id: str, location: str, dataset_id: str
) -> Dict[str, Any]:
    """Gets the IAM policy for the specified dataset.

    See
    https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/datasets
    before running the sample.
    See https://googleapis.github.io/google-api-python-client/docs/dyn/healthcare_v1.projects.locations.datasets.html#getIamPolicy
    for the Python API reference.

    Args:
      project_id: The project ID or project number of the Google Cloud project you want
          to use.
      location: The name of the dataset's location.
      dataset_id: The ID of the dataset containing the IAM policy to get.

    Returns:
      A dictionary representing an IAM policy.
    """
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
    dataset_name = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )

    request = (
        client.projects().locations().datasets().getIamPolicy(resource=dataset_name)
    )

    try:
        response = request.execute()
        print("etag: {}".format(response.get("name")))
        return response
    except HttpError as err:
        raise err


# [END healthcare_dataset_get_iam_policy]
