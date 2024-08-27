# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This file contains code samples that demonstrate how to set policy for project.

# [START iam_set_policy]
from google.cloud import resourcemanager_v3
from google.iam.v1 import iam_policy_pb2, policy_pb2


def set_project_policy(
    project_id: str, policy: policy_pb2.Policy, merge: bool = True
) -> policy_pb2.Policy:
    """
    Set policy for project. Pay attention that previous state will be completely rewritten.
    If you want to update only part of the policy follow the approach read->modify->write.
    For more details about policies check out https://cloud.google.com/iam/docs/policies

    project_id: ID or number of the Google Cloud project you want to use.
    policy: Policy which has to be set.
    merge: The strategy to be used forming the request. CopyFrom is clearing both mutable and immutable fields,
    when MergeFrom is replacing only immutable fields and extending mutable.
    https://googleapis.dev/python/protobuf/latest/google/protobuf/message.html#google.protobuf.message.Message.CopyFrom
    """
    client = resourcemanager_v3.ProjectsClient()

    request = iam_policy_pb2.GetIamPolicyRequest()
    request.resource = f"projects/{project_id}"
    current_policy = client.get_iam_policy(request)

    # Etag should as fresh as possible to lower chance of collisions
    policy.ClearField("etag")
    if merge:
        current_policy.MergeFrom(policy)
    else:
        current_policy.CopyFrom(policy)

    request = iam_policy_pb2.SetIamPolicyRequest()
    request.resource = f"projects/{project_id}"

    # request.etag field also will be merged which means you are secured from collision,
    # but it means that request may fail and you need to leverage exponential retries approach
    # to be sure policy has been updated.
    request.policy.CopyFrom(current_policy)

    policy = client.set_iam_policy(request)
    return policy


# [END iam_set_policy]


if __name__ == "__main__":
    # To run the sample you would need
    # resourcemanager.projects.setIamPolicy (roles/resourcemanager.projectIamAdmin)

    # Your Google Cloud project ID.
    project_id = "test-project-id"

    new_policy = policy_pb2.Policy()
    binding = policy_pb2.Binding()
    binding.role = "roles/viewer"
    binding.members.append(
        f"serviceAccount:test-service-account@{project_id}.iam.gserviceaccount.com"
    )
    new_policy.bindings.append(binding)

    set_project_policy(project_id, new_policy)
