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

# [START privateca_create_ca_pool]
import google.cloud.security.privateca_v1 as privateca_v1


def create_ca_pool(project_id: str, location: str, ca_pool_name: str) -> None:
    """
    Create a Certificate Authority pool. All certificates created under this CA pool will
    follow the same issuance policy, IAM policies,etc.,

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        location: location you want to use. For a list of locations, see: https://cloud.google.com/certificate-authority-service/docs/locations.
        ca_pool_name: a unique name for the ca pool.
    """

    caServiceClient = privateca_v1.CertificateAuthorityServiceClient()

    ca_pool = privateca_v1.CaPool(
        # Set the tier (see: https://cloud.google.com/certificate-authority-service/docs/tiers).
        tier=privateca_v1.CaPool.Tier.ENTERPRISE,
    )
    location_path = caServiceClient.common_location_path(project_id, location)

    # Create the pool request.
    request = privateca_v1.CreateCaPoolRequest(
        parent=location_path, ca_pool_id=ca_pool_name, ca_pool=ca_pool,
    )

    # Create the CA pool.
    operation = caServiceClient.create_ca_pool(request=request)

    print("Operation result:", operation.result())


# [END privateca_create_ca_pool]
