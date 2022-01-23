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

# [START privateca_filter_certificate]
import google.cloud.security.privateca_v1 as privateca_v1


def filter_certificates(
    project_id: str, location: str, ca_pool_name: str, filter_condition: str
) -> None:
    """
    Filter certificates based on a condition and list them.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        location: location you want to use. For a list of locations, see: https://cloud.google.com/certificate-authority-service/docs/locations.
        ca_pool_name: name of the CA pool which contains the certificates to be listed.
    """

    caServiceClient = privateca_v1.CertificateAuthorityServiceClient()

    ca_pool_path = caServiceClient.ca_pool_path(project_id, location, ca_pool_name)

    # Create the certificate request and set the filter condition.
    request = privateca_v1.ListCertificatesRequest(
        parent=ca_pool_path, filter=filter_condition,
    )

    # Retrieve and print the certificate names.
    print("Available certificates: ")
    for cert in caServiceClient.list_certificates(request=request):
        print(f"- {cert.name}")


# [END privateca_filter_certificate]
