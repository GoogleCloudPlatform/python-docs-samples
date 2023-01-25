#!/usr/bin/env python

# Copyright 2021 Google LLC
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

# [START privateca_list_ca_pool]
import google.cloud.security.privateca_v1 as privateca_v1


def list_ca_pools(project_id: str, location: str) -> None:
    """
    List all CA pools present in the given project and location.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        location: location you want to use. For a list of locations, see: https://cloud.google.com/certificate-authority-service/docs/locations.
    """

    caServiceClient = privateca_v1.CertificateAuthorityServiceClient()

    location_path = caServiceClient.common_location_path(project_id, location)

    request = privateca_v1.ListCaPoolsRequest(parent=location_path)

    print("Available CA pools:")

    for ca_pool in caServiceClient.list_ca_pools(request=request):
        ca_pool_name = ca_pool.name
        # ca_pool.name represents the full resource name of the
        # format 'projects/{project-id}/locations/{location}/ca-pools/{ca-pool-name}'.
        # Hence stripping it down to just pool name.
        print(caServiceClient.parse_ca_pool_path(ca_pool_name)["ca_pool"])


# [END privateca_list_ca_pool]
