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

# [START privateca_update_ca_label]
import google.cloud.security.privateca_v1 as privateca_v1
from google.protobuf import field_mask_pb2


def update_ca_label(
    project_id: str,
    location: str,
    ca_pool_name: str,
    ca_name: str,
) -> None:
    """
    Update the labels in a certificate authority.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        location: location you want to use. For a list of locations, see: https://cloud.google.com/certificate-authority-service/docs/locations.
        ca_pool_name: set it to the CA Pool under which the CA should be updated.
        ca_name: unique name for the CA.
    """

    caServiceClient = privateca_v1.CertificateAuthorityServiceClient()

    # Set the parent path and the new labels.
    ca_parent = caServiceClient.certificate_authority_path(
        project_id, location, ca_pool_name, ca_name
    )
    certificate_authority = privateca_v1.CertificateAuthority(
        name=ca_parent,
        labels={"env": "test"},
    )

    # Create a request to update the CA.
    request = privateca_v1.UpdateCertificateAuthorityRequest(
        certificate_authority=certificate_authority,
        update_mask=field_mask_pb2.FieldMask(paths=["labels"]),
    )

    operation = caServiceClient.update_certificate_authority(request=request)
    result = operation.result()

    print("Operation result:", result)

    # Get the updated CA and check if it contains the new label.

    certificate_authority = caServiceClient.get_certificate_authority(name=ca_parent)

    if (
        "env" in certificate_authority.labels
        and certificate_authority.labels["env"] == "test"
    ):
        print("Successfully updated the labels !")


# [END privateca_update_ca_label]
