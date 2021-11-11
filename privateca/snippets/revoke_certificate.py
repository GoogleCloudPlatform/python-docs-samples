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

import sys

# [START privateca_revoke_certificate]

import google.cloud.security.privateca_v1 as privateca_v1


def revoke_certificate(
    project_id: str, location: str, ca_pool_name: str, certificate_name: str,
) -> None:
    """
    Revoke an issued certificate. Once revoked, the certificate will become invalid and will expire post its lifetime.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        location: location you want to use. For a list of locations, see: https://cloud.google.com/certificate-authority-service/docs/locations.
        ca_pool_name: name for the CA pool which contains the certificate.
        certificate_name: name of the certificate to be revoked.
    """

    caServiceClient = privateca_v1.CertificateAuthorityServiceClient()

    # Create Certificate Path.
    certificate_path = caServiceClient.certificate_path(
        project_id, location, ca_pool_name, certificate_name
    )

    # Create Revoke Certificate Request and specify the appropriate revocation reason.
    request = privateca_v1.RevokeCertificateRequest(
        name=certificate_path, reason=privateca_v1.RevocationReason.PRIVILEGE_WITHDRAWN
    )
    result = caServiceClient.revoke_certificate(request=request)

    print("Certificate revoke result:", result)


# [END privateca_revoke_certificate]

if __name__ == "__main__":
    revoke_certificate(
        project_id=sys.argv[1],
        location=sys.argv[2],
        ca_pool_name=sys.argv[3],
        certificate_name=sys.argv[4],
    )
