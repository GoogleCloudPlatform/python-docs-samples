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

# [START privateca_update_certificate_template]
import google.cloud.security.privateca_v1 as privateca_v1
from google.protobuf import field_mask_pb2


def update_certificate_template(
    project_id: str, location: str, certificate_template_id: str,
) -> None:
    """
    Update an existing certificate template.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        location: location you want to use. For a list of locations, see: https://cloud.google.com/certificate-authority-service/docs/locations.
        certificate_template_id: set a unique name for the certificate template.
    """

    caServiceClient = privateca_v1.CertificateAuthorityServiceClient()

    certificate_name = caServiceClient.certificate_template_path(
        project_id, location, certificate_template_id,
    )

    # Set the parent name and the properties to be updated.
    certificate_template = privateca_v1.CertificateTemplate(
        name=certificate_name,
        identity_constraints=privateca_v1.CertificateIdentityConstraints(
            allow_subject_passthrough=False, allow_subject_alt_names_passthrough=True,
        ),
    )

    # Set the mask corresponding to the properties updated above.
    field_mask = field_mask_pb2.FieldMask(
        paths=[
            "identity_constraints.allow_subject_alt_names_passthrough",
            "identity_constraints.allow_subject_passthrough",
        ],
    )

    # Set the new template.
    # Set the mask to specify which properties of the template should be updated.
    request = privateca_v1.UpdateCertificateTemplateRequest(
        certificate_template=certificate_template, update_mask=field_mask,
    )
    operation = caServiceClient.update_certificate_template(request=request)
    result = operation.result()

    print("Operation result", result)

    # Get the updated certificate template and check if the properties have been updated.
    cert_identity_constraints = caServiceClient.get_certificate_template(
        name=certificate_name
    ).identity_constraints

    if (
        not cert_identity_constraints.allow_subject_passthrough
        and cert_identity_constraints.allow_subject_alt_names_passthrough
    ):
        print("Successfully updated the certificate template!")
        return

    print("Error in updating certificate template!")


# [END privateca_update_certificate_template]
