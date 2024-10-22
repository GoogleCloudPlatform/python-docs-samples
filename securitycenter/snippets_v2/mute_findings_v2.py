#!/usr/bin/env python
#
# Copyright 2024 Google LLC
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


# [START securitycenter_set_mute_v2]
def set_mute_finding(finding_path: str) -> None:
    """
      Mute an individual finding.
      If a finding is already muted, muting it again has no effect.
      Various mute states are: MUTE_UNSPECIFIED/MUTE/UNMUTE.
    Args:
        finding_path: The relative resource name of the finding. See:
        https://cloud.google.com/apis/design/resource_names#relative_resource_name
        Use any one of the following formats:
        - organizations/{organization_id}/sources/{source_id}/finding/{finding_id},
        - folders/{folder_id}/sources/{source_id}/finding/{finding_id},
        - projects/{project_id}/sources/{source_id}/finding/{finding_id}.
    """
    from google.cloud import securitycenter_v2

    client = securitycenter_v2.SecurityCenterClient()

    request = securitycenter_v2.SetMuteRequest()
    request.name = finding_path
    request.mute = securitycenter_v2.Finding.Mute.MUTED

    finding = client.set_mute(request)
    print(f"Mute value for the finding: {finding.mute.name}")
    return finding


# [END securitycenter_set_mute_v2]


# [START securitycenter_set_unmute_v2]
def set_unmute_finding(finding_path: str) -> None:
    """
      Unmute an individual finding.
      Unmuting a finding that isn't muted has no effect.
      Various mute states are: MUTE_UNSPECIFIED/MUTE/UNMUTE.
    Args:
        finding_path: The relative resource name of the finding. See:
        https://cloud.google.com/apis/design/resource_names#relative_resource_name
        Use any one of the following formats:
        - organizations/{organization_id}/sources/{source_id}/finding/{finding_id},
        - folders/{folder_id}/sources/{source_id}/finding/{finding_id},
        - projects/{project_id}/sources/{source_id}/finding/{finding_id}.
    """
    from google.cloud import securitycenter_v2

    client = securitycenter_v2.SecurityCenterClient()

    request = securitycenter_v2.SetMuteRequest()
    request.name = finding_path
    request.mute = securitycenter_v2.Finding.Mute.UNMUTED

    finding = client.set_mute(request)
    print(f"Mute value for the finding: {finding.mute.name}")
    return finding


# [END securitycenter_set_unmute_v2]


# [START securitycenter_bulk_mute_v2]
def bulk_mute_findings(parent_path: str, location_id: str, mute_rule: str) -> None:
    """
      Kicks off a long-running operation (LRO) to bulk mute findings for a parent based on a filter.

      The parent can be either an organization, folder, or project. The findings
      matched by the filter will be muted after the LRO is done.

    Args:
        parent_path: Used to specify the resource under which the mute rule operates.
          Use any one of the following options:
            - organizations/{organization}
            - folders/{folder}
            - projects/{project}
        location_id: The Google Cloud location ID, for example: 'global'.
        mute_rule: Expression that identifies findings that should be updated.
    """
    from google.cloud import securitycenter_v2

    client = securitycenter_v2.SecurityCenterClient()

    request = securitycenter_v2.BulkMuteFindingsRequest(
        parent=f"{parent_path}/locations/{location_id}",
        # To create mute rules, see:
        # https://cloud.google.com/security-command-center/docs/how-to-mute-findings#create_mute_rules
        filter=mute_rule,
    )

    response = client.bulk_mute_findings(request)
    print(f"Bulk mute findings completed successfully: {response}")
    return response


# [END securitycenter_bulk_mute_v2]
