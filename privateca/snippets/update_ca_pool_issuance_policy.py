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

# [START privateca_set_issuance_policy]
import google.cloud.security.privateca_v1 as privateca_v1
from google.protobuf import field_mask_pb2
from google.type import expr_pb2


def update_ca_pool_issuance_policy(
    project_id: str,
    location: str,
    ca_pool_name: str,
) -> None:
    """
    Update the issuance policy for a CA Pool. All certificates issued from this CA Pool should
    meet the issuance policy

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        location: location you want to use. For a list of locations, see: https://cloud.google.com/certificate-authority-service/docs/locations.
        ca_pool_name: a unique name for the ca pool.
    """

    caServiceClient = privateca_v1.CertificateAuthorityServiceClient()

    ca_pool_path = caServiceClient.ca_pool_path(project_id, location, ca_pool_name)

    # Set the updated issuance policy for the CA Pool.
    # This particular issuance policy allows only SANs that
    # have DNS Names as "us.google.org" or ending in ".google.com". */
    expr = expr_pb2.Expr(
        expression='subject_alt_names.all(san, san.type == DNS && (san.value == "us.google.org" || san.value.endsWith(".google.com")) )'
    )

    issuance_policy = privateca_v1.CaPool.IssuancePolicy(
        identity_constraints=privateca_v1.CertificateIdentityConstraints(
            allow_subject_passthrough=True,
            allow_subject_alt_names_passthrough=True,
            cel_expression=expr,
        ),
    )

    ca_pool = privateca_v1.CaPool(
        name=ca_pool_path,
        issuance_policy=issuance_policy,
    )

    # 1. Set the CA pool with updated values.
    # 2. Set the update mask to specify which properties of the CA Pool should be updated.
    # Only the properties specified in the mask will be updated. Make sure that the mask fields
    # match the updated issuance policy.
    # For more info on constructing path for update mask, see:
    # https://cloud.google.com/certificate-authority-service/docs/reference/rest/v1/projects.locations.caPools#issuancepolicy */
    request = privateca_v1.UpdateCaPoolRequest(
        ca_pool=ca_pool,
        update_mask=field_mask_pb2.FieldMask(
            paths=[
                "issuance_policy.identity_constraints.allow_subject_alt_names_passthrough",
                "issuance_policy.identity_constraints.allow_subject_passthrough",
                "issuance_policy.identity_constraints.cel_expression",
            ],
        ),
    )
    operation = caServiceClient.update_ca_pool(request=request)
    result = operation.result()

    print("Operation result", result)

    # Get the CA Pool's issuance policy and verify if the fields have been successfully updated.
    issuance_policy = caServiceClient.get_ca_pool(name=ca_pool_path).issuance_policy

    # Similarly, you can check for other modified fields as well.
    if (
        issuance_policy.identity_constraints.allow_subject_passthrough
        and issuance_policy.identity_constraints.allow_subject_alt_names_passthrough
    ):
        print("CA Pool Issuance policy has been updated successfully!")
        return

    print("Error in updating CA Pool Issuance policy! Please try again!")


# [END privateca_set_issuance_policy]
