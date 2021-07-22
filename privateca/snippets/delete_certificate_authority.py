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

# [START privateca_delete_ca]
import google.cloud.security.privateca_v1 as privateca_v1


def delete_certificate_authority(
    project_id: str, location: str, ca_pool_name: str, ca_name: str
) -> None:
    """
    Delete the Certificate Authority from the specified CA pool.
    Before deletion, the CA must be disabled and must not contain any active certificates.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        location: location you want to use. For a list of locations, see: https://cloud.google.com/certificate-authority-service/docs/locations.
        ca_pool_name: the name of the CA pool under which the CA is present.
        ca_name: the name of the CA to be deleted.
    """

    caServiceClient = privateca_v1.CertificateAuthorityServiceClient()
    ca_path = caServiceClient.certificate_authority_path(
        project_id, location, ca_pool_name, ca_name
    )

    # Check if the CA is enabled.
    ca_state = caServiceClient.get_certificate_authority(name=ca_path).state
    print(ca_state)
    if ca_state == privateca_v1.CertificateAuthority.State.ENABLED:
        print(
            "Please disable the Certificate Authority before deletion ! Current state:",
            ca_state,
        )

    # Create the DeleteCertificateAuthorityRequest.
    # Setting the ignore_active_certificates to True will delete the CA
    # even if it contains active certificates. Care should be taken to re-anchor
    # the certificates to new CA before deleting.
    request = privateca_v1.DeleteCertificateAuthorityRequest(
        name=ca_path, ignore_active_certificates=False
    )

    # Delete the Certificate Authority.
    operation = caServiceClient.delete_certificate_authority(request=request)
    result = operation.result()

    print("Operation result", result)

    # Get the current CA state.
    ca_state = caServiceClient.get_certificate_authority(name=ca_path).state

    # Check if the CA has been deleted.
    if ca_state == privateca_v1.CertificateAuthority.State.DELETED:
        print("Successfully deleted Certificate Authority:", ca_name)
    else:
        print(
            "Unable to delete Certificate Authority. Please try again ! Current state:",
            ca_state,
        )


# [END privateca_delete_ca]
