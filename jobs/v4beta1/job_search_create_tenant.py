# Copyright 2020 Google LLC
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

# [START job_search_create_tenant]

from google.cloud import talent
import six


def create_tenant(project_id, external_id):
    """Create Tenant for scoping resources, e.g. companies and jobs"""

    client = talent.TenantServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # external_id = 'Your Unique Identifier for Tenant'

    if isinstance(project_id, six.binary_type):
        project_id = project_id.decode("utf-8")
    if isinstance(external_id, six.binary_type):
        external_id = external_id.decode("utf-8")
    parent = client.project_path(project_id)
    tenant = {"external_id": external_id}

    response = client.create_tenant(parent, tenant)
    print("Created Tenant")
    print("Name: {}".format(response.name))
    print("External ID: {}".format(response.external_id))
    return response.name


# [END job_search_create_tenant]
