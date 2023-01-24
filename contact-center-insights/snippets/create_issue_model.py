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
#
# [START contactcenterinsights_create_issue_model]
from google.cloud import contact_center_insights_v1


def create_issue_model(project_id: str) -> contact_center_insights_v1.IssueModel:
    """Creates an issue model.

    Args:
        project_id:
            The project identifier. For example, 'my-project'.

    Returns:
        An issue model.
    """
    # Construct a parent resource.
    parent = (
        contact_center_insights_v1.ContactCenterInsightsClient.common_location_path(
            project_id, "us-central1"
        )
    )

    # Construct an issue model.
    issue_model = contact_center_insights_v1.IssueModel()
    issue_model.display_name = "my-model"
    issue_model.input_data_config.filter = 'medium="CHAT"'

    # Call the Insights client to create an issue model.
    insights_client = contact_center_insights_v1.ContactCenterInsightsClient()
    issue_model_operation = insights_client.create_issue_model(
        parent=parent, issue_model=issue_model
    )

    issue_model = issue_model_operation.result(timeout=86400)
    print(f"Created an issue model named {issue_model.name}")
    return issue_model


# [END contactcenterinsights_create_issue_model]
