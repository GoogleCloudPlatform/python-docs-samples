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

# [START privateca_create_certificate_csr]
import google.cloud.security.privateca_v1 as privateca_v1
from google.protobuf import duration_pb2


def create_certificate_csr(
    project_id: str,
    location: str,
    ca_pool_name: str,
    ca_name: str,
    certificate_name: str,
    certificate_lifetime: int,
    pem_csr: str,
) -> None:
    """
    Create a Certificate which is issued by the specified Certificate Authority (CA).
    The certificate details and the public key is provided as a Certificate Signing Request (CSR).
    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        location: location you want to use. For a list of locations, see: https://cloud.google.com/certificate-authority-service/docs/locations.
        ca_pool_name: set a unique name for the CA pool.
        ca_name: the name of the certificate authority to sign the CSR.
        certificate_name: set a unique name for the certificate.
        certificate_lifetime: the validity of the certificate in seconds.
        pem_csr: set the Certificate Issuing Request in the pem encoded format.
    """

    ca_service_client = privateca_v1.CertificateAuthorityServiceClient()

    # The public key used to sign the certificate can be generated using any crypto library/framework.
    # Also you can use Cloud KMS to retrieve an already created public key.
    # For more info, see: https://cloud.google.com/kms/docs/retrieve-public-key.

    # Create certificate with CSR.
    # The pem_csr contains the public key and the domain details required.
    certificate = privateca_v1.Certificate(
        pem_csr=pem_csr,
        lifetime=duration_pb2.Duration(seconds=certificate_lifetime),
    )

    # Create the Certificate Request.
    # Set the CA which is responsible for creating the certificate with the provided CSR.
    request = privateca_v1.CreateCertificateRequest(
        parent=ca_service_client.ca_pool_path(project_id, location, ca_pool_name),
        certificate_id=certificate_name,
        certificate=certificate,
        issuing_certificate_authority_id=ca_name,
    )
    response = ca_service_client.create_certificate(request=request)

    print(f"Certificate created successfully: {response.name}")

    # Get the signed certificate and the issuer chain list.
    print(f"Signed certificate: {response.pem_certificate}")
    print(f"Issuer chain list: {response.pem_certificate_chain}")


# [END privateca_create_certificate_csr]
