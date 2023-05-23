# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START compute_certificate_create]
from __future__ import annotations

from pathlib import Path
from pprint import pprint

from googleapiclient import discovery


def create_certificate(
    project_id: str, certificate_file: str | Path, private_key_file: str | Path, certificate_name: str, description: str = "Certificate created from a code sample."
) -> None:
    """
    Create a global SSL self-signed certificate within your Google Cloud project.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        certificate_file: path to the file with the certificate you want to create in your project.
        private_key_file: path to the private key you used to sign the certificate with.
        certificate_name: name for the certificate once it's created in your project.
        description: description of the certificate.
    """
    service = discovery.build("compute", "v1")

    # Read the cert into memory
    with open(certificate_file) as f:
        _temp_cert = f.read()

    # Read the private_key into memory
    with open(private_key_file) as f:
        _temp_key = f.read()

    # Now that the certificate and private key are in memory, you can create the
    # certificate resource
    ssl_certificate_body = {
        "name": certificate_name,
        "description": description,
        "certificate": _temp_cert,
        "privateKey": _temp_key,
    }
    request = service.sslCertificates().insert(
        project=project_id, body=ssl_certificate_body
    )
    response = request.execute()
    pprint(response)


# [END compute_certificate_create]
