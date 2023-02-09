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

# [START privateca_list_certificate_template]
import google.cloud.security.privateca_v1 as privateca_v1


def list_certificate_templates(project_id: str, location: str) -> None:
    """
    List the certificate templates present in the given project and location.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        location: location you want to use. For a list of locations, see: https://cloud.google.com/certificate-authority-service/docs/locations.
    """

    caServiceClient = privateca_v1.CertificateAuthorityServiceClient()

    # List Templates Request.
    request = privateca_v1.ListCertificateTemplatesRequest(
        parent=caServiceClient.common_location_path(project_id, location),
    )

    print("Available certificate templates:")
    for certificate_template in caServiceClient.list_certificate_templates(
        request=request
    ):
        print(certificate_template.name)


# [END privateca_list_certificate_template]
