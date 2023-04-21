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

# [START privateca_disable_ca]
import google.cloud.security.privateca_v1 as privateca_v1


def disable_certificate_authority(
    project_id: str, location: str, ca_pool_name: str, ca_name: str
) -> None:
    """
    Disable a Certificate Authority which is present in the given CA pool.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        location: location you want to use. For a list of locations, see: https://cloud.google.com/certificate-authority-service/docs/locations.
        ca_pool_name: the name of the CA pool under which the CA is present.
        ca_name: the name of the CA to be disabled.
    """

    caServiceClient = privateca_v1.CertificateAuthorityServiceClient()
    ca_path = caServiceClient.certificate_authority_path(
        project_id, location, ca_pool_name, ca_name
    )

    # Create the Disable Certificate Authority Request.
    request = privateca_v1.DisableCertificateAuthorityRequest(name=ca_path)

    # Disable the Certificate Authority.
    operation = caServiceClient.disable_certificate_authority(request=request)
    result = operation.result()

    # Get the current CA state.
    ca_state = caServiceClient.get_certificate_authority(name=ca_path).state

    # Check if the CA is disabled.
    if ca_state == privateca_v1.CertificateAuthority.State.DISABLED:
        print("Disabled Certificate Authority:", ca_name)
    else:
        print("Cannot disable the Certificate Authority ! Current CA State:", ca_state)


# [END privateca_disable_ca]
