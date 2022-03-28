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

# [START privateca_delete_certificate_template]
import google.cloud.security.privateca_v1 as privateca_v1


def delete_certificate_template(
    project_id: str,
    location: str,
    certificate_template_id: str,
) -> None:
    """
    Delete the certificate template present in the given project and location.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        location: location you want to use. For a list of locations, see: https://cloud.google.com/certificate-authority-service/docs/locations.
        certificate_template_id: set a unique name for the certificate template.
    """

    caServiceClient = privateca_v1.CertificateAuthorityServiceClient()

    # Request to delete a certificate template.
    request = privateca_v1.DeleteCertificateTemplateRequest(
        name=caServiceClient.certificate_template_path(
            project_id,
            location,
            certificate_template_id,
        )
    )
    operation = caServiceClient.delete_certificate_template(request=request)
    result = operation.result()

    print("Operation result", result)
    print("Deleted certificate template:", certificate_template_id)


# [END privateca_delete_certificate_template]
