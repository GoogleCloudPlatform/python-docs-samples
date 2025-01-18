#!/usr/bin/env python
# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Example of verifying Google Compute Engine virtual machine identity.

This sample will work only on a GCE virtual machine, as it relies on
communication with metadata server
(https://cloud.google.com/compute/docs/storing-retrieving-metadata).

Example is used on:
https://cloud.google.com/compute/docs/instances/verifying-instance-identity
"""
import pprint

# [START compute_vm_identity_verify_token]
import google.auth.transport.requests
from google.oauth2 import id_token
# [END compute_vm_identity_verify_token]

# [START compute_vm_identity_acquire_token]
import requests

AUDIENCE_URL = "http://www.example.com"
METADATA_HEADERS = {"Metadata-Flavor": "Google"}
METADATA_VM_IDENTITY_URL = (
    "http://metadata.google.internal/computeMetadata/v1/"
    "instance/service-accounts/default/identity?"
    "audience={audience}&format={format}&licenses={licenses}"
)
FORMAT = "full"
LICENSES = "TRUE"


def acquire_token(
    audience: str = AUDIENCE_URL, format: str = "standard", licenses: bool = True
) -> str:
    """
    Requests identity information from the metadata server.

    Args:
        audience: the unique URI agreed upon by both the instance and the
            system verifying the instance's identity. For example, the audience
            could be a URL for the connection between the two systems.
        format: the optional parameter that specifies whether the project and
            instance details are included in the payload. Specify `full` to
            include this information in the payload or standard to omit the
            information from the payload. The default value is `standard`.
        licenses: an optional parameter that specifies whether license
            codes for images associated with this instance are included in the
            payload. Specify TRUE to include this information or FALSE to omit
            this information from the payload. The default value is FALSE.
            Has no effect unless format is `full`.

    Returns:
        A JSON Web Token signed using the RS256 algorithm. The token includes a
        Google signature and additional information in the payload. You can send
        this token to other systems and applications so that they can verify the
        token and confirm that the identity of your instance.
    """
    # Construct a URL with the audience and format.
    url = METADATA_VM_IDENTITY_URL.format(
        audience=audience, format=format, licenses=licenses
    )

    # Request a token from the metadata server.
    r = requests.get(url, headers=METADATA_HEADERS)
    # Extract and return the token from the response.
    r.raise_for_status()
    return r.text
# [END compute_vm_identity_acquire_token]


# [START compute_vm_identity_verify_token]
def verify_token(token: str, audience: str) -> dict:
    """Verify token signature and return the token payload.

    Args:
        token: the JSON Web Token received from the metadata server to
            be verified.
        audience: the unique URI agreed upon by both the instance and the
            system verifying the instance's identity.

    Returns:
        Dictionary containing the token payload.
    """
    request = google.auth.transport.requests.Request()
    payload = id_token.verify_token(token, request=request, audience=audience)
    return payload
# [END compute_vm_identity_verify_token]


if __name__ == "__main__":
    token_ = acquire_token(AUDIENCE_URL)
    print("Received token:", token_)
    print("Token verification:")
    pprint.pprint(verify_token(token_, AUDIENCE_URL))
