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


# [START healthcare_dataset_set_iam_policy]
# Imports the Dict and Any types for runtime type hints.
from typing import Any, Dict

# [END healthcare_dataset_set_iam_policy]


# [START healthcare_dataset_set_iam_policy]
def set_dataset_iam_policy(
    project_id: str,
    location: str,
    dataset_id: str,
    member: str,
    role: str,
    etag: str = None,
) -> Dict[str, Any]:
    """Sets the IAM policy for the specified dataset.

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

    See
    https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/datasets
    before running the sample.
    See https://googleapis.github.io/google-api-python-client/docs/dyn/healthcare_v1.projects.locations.datasets.html#setIamPolicy
    for the Python API reference.

    Args:
      project_id: The project ID or project number of the Google Cloud project you want
          to use.
      location: The name of the dataset's location.
      dataset_id: The ID of the dataset containing the IAM policy to set.
      member: The principals to grant access for a Google Cloud resource.
      role: The role to assign to the list of 'members'.
      etag: The 'etag' returned in a previous getIamPolicy request to ensure that
        setIamPolicy changes apply to the same policy version.

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

    # TODO(developer): Uncomment these lines and replace with your values.
    # role = 'roles/viewer'
    # member = 'serviceAccount:group@example.com'
    policy = {"bindings": [{"role": role, "members": [member]}]}

    if etag is not None:
        policy["etag"] = etag

    request = (
        client.projects()
        .locations()
        .datasets()
        .setIamPolicy(resource=dataset_name, body={"policy": policy})
    )
    try:
        response = request.execute()
        print("etag: {}".format(response.get("name")))
        print("bindings: {}".format(response.get("bindings")))
        return response
    except HttpError as err:
        raise err


# [END healthcare_dataset_set_iam_policy]
