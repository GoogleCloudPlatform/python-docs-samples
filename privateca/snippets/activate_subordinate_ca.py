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

# [START privateca_activate_subordinateca]
import google.cloud.security.privateca_v1 as privateca_v1


def activate_subordinate_ca(
    project_id: str,
    location: str,
    ca_pool_name: str,
    subordinate_ca_name: str,
    pem_ca_certificate: str,
    ca_name: str,
) -> None:
    """
    Activate a subordinate Certificate Authority (CA).
    *Prerequisite*: Get the Certificate Signing Resource (CSR) of the subordinate CA signed by another CA. Pass in the signed
    certificate and (issuer CA's name or the issuer CA's Certificate chain).
    *Post*: After activating the subordinate CA, it should be enabled before issuing certificates.
    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        location: location you want to use. For a list of locations, see: https://cloud.google.com/certificate-authority-service/docs/locations.
        ca_pool_name: set it to the CA Pool under which the CA should be created.
        pem_ca_certificate: the signed certificate, obtained by signing the CSR.
        subordinate_ca_name: the CA to be activated.
        ca_name: The name of the certificate authority which signed the CSR.
            If an external CA (CA not present in Google Cloud) was used for signing,
            then use the CA's issuerCertificateChain.
    """

    ca_service_client = privateca_v1.CertificateAuthorityServiceClient()

    subordinate_ca_path = ca_service_client.certificate_authority_path(
        project_id, location, ca_pool_name, subordinate_ca_name
    )
    ca_path = ca_service_client.certificate_authority_path(
        project_id, location, ca_pool_name, ca_name
    )

    # Set CA subordinate config.
    subordinate_config = privateca_v1.SubordinateConfig(
        # Follow one of the below methods:
        # Method 1: If issuer CA is in Google Cloud, set the Certificate Authority Name.
        certificate_authority=ca_path,
        # Method 2: If issuer CA is external to Google Cloud, set the issuer's certificate chain.
        # The certificate chain of the CA (which signed the CSR) from leaf to root.
        # pem_issuer_chain=privateca_v1.SubordinateConfig.SubordinateConfigChain(
        #     pem_certificates=issuer_certificate_chain,
        # )
    )

    # Construct the "Activate CA Request".
    request = privateca_v1.ActivateCertificateAuthorityRequest(
        name=subordinate_ca_path,
        # The signed certificate.
        pem_ca_certificate=pem_ca_certificate,
        subordinate_config=subordinate_config,
    )

    # Activate the CA
    operation = ca_service_client.activate_certificate_authority(request=request)
    result = operation.result()

    print("Operation result:", result)

    # The current state will be STAGED.
    # The Subordinate CA has to be ENABLED before issuing certificates.
    print(
        f"Current state: {ca_service_client.get_certificate_authority(name=subordinate_ca_path).state}"
    )


# [END privateca_activate_subordinateca]
