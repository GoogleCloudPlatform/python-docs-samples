#!/usr/bin/env python

# Copyright 2022 Google LLC
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

# [START privateca_create_certificate_template]
import google.cloud.security.privateca_v1 as privateca_v1
from google.type import expr_pb2


def create_certificate_template(
    project_id: str,
    location: str,
    certificate_template_id: str,
) -> None:
    """
    Create a Certificate template. These templates can be reused for common
    certificate issuance scenarios.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        location: location you want to use. For a list of locations, see: https://cloud.google.com/certificate-authority-service/docs/locations.
        certificate_template_id: set a unique name for the certificate template.
    """

    caServiceClient = privateca_v1.CertificateAuthorityServiceClient()

    # Describes any predefined X.509 values set by this template.
    # The provided extensions are copied over to certificate requests that use this template.
    x509_parameters = privateca_v1.X509Parameters(
        key_usage=privateca_v1.KeyUsage(
            base_key_usage=privateca_v1.KeyUsage.KeyUsageOptions(
                digital_signature=True,
                key_encipherment=True,
            ),
            extended_key_usage=privateca_v1.KeyUsage.ExtendedKeyUsageOptions(
                server_auth=True,
            ),
        ),
        ca_options=privateca_v1.X509Parameters.CaOptions(
            is_ca=False,
        ),
    )

    # CEL expression that is evaluated against the Subject and
    # Subject Alternative Name of the certificate before it is issued.
    expr = expr_pb2.Expr(expression="subject_alt_names.all(san, san.type == DNS)")

    # Set the certificate issuance schema.
    certificate_template = privateca_v1.CertificateTemplate(
        predefined_values=x509_parameters,
        identity_constraints=privateca_v1.CertificateIdentityConstraints(
            cel_expression=expr,
            allow_subject_passthrough=False,
            allow_subject_alt_names_passthrough=False,
        ),
    )

    # Request to create a certificate template.
    request = privateca_v1.CreateCertificateTemplateRequest(
        parent=caServiceClient.common_location_path(project_id, location),
        certificate_template=certificate_template,
        certificate_template_id=certificate_template_id,
    )
    operation = caServiceClient.create_certificate_template(request=request)
    result = operation.result()

    print("Operation result:", result)


# [END privateca_create_certificate_template]
