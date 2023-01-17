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
# [START contactcenterinsights_create_analysis]
from google.cloud import contact_center_insights_v1


def create_analysis(conversation_name: str) -> contact_center_insights_v1.Analysis:
    """Creates an analysis.

    Args:
        conversation_name:
            The parent resource of the analysis.
            Format is 'projects/{project_id}/locations/{location_id}/conversations/{conversation_id}'.
            For example, 'projects/my-project/locations/us-central1/conversations/123456789'.

    Returns:
        An analysis.
    """
    # Construct an analysis.
    analysis = contact_center_insights_v1.Analysis()

    # Call the Insights client to create an analysis.
    insights_client = contact_center_insights_v1.ContactCenterInsightsClient()
    analysis_operation = insights_client.create_analysis(
        parent=conversation_name, analysis=analysis
    )
    analysis = analysis_operation.result(timeout=86400)
    print(f"Created {analysis.name}")
    return analysis


# [END contactcenterinsights_create_analysis]
