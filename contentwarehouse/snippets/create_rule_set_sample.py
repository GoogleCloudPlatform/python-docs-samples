# Copyright 2023 Google LLC
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


# [START contentwarehouse_create_rule_set]

from google.cloud import contentwarehouse

# TODO(developer): Uncomment these variables before running the sample.
# project_number = "YOUR_PROJECT_NUMBER"
# location = "us" # Format is 'us' or 'eu'


def create_rule_set(project_number: str, location: str) -> None:
    # Create a client
    client = contentwarehouse.RuleSetServiceClient()

    # The full resource name of the location, e.g.:
    # projects/{project_number}/locations/{location}
    parent = client.common_location_path(project=project_number, location=location)

    enable_hard_delete = contentwarehouse.DeleteDocumentAction(enable_hard_delete=True)

    actions = contentwarehouse.Action(delete_document_action=enable_hard_delete)

    rules = contentwarehouse.Rule(
        trigger_type="ON_CREATE",
        condition="documentType == 'W9' && STATE =='CA'",
        actions=[actions],
    )

    rule_set = contentwarehouse.RuleSet(
        description="W9: Basic validation check rules.",
        source="My Organization",
        rules=[rules],
    )

    # Initialize request argument(s)
    request = contentwarehouse.CreateRuleSetRequest(parent=parent, rule_set=rule_set)

    # Make the request
    response = client.create_rule_set(request=request)

    # Handle the response
    print(f"Rule Set Created: {response}")

    # Initialize request argument(s)
    request = contentwarehouse.ListRuleSetsRequest(
        parent=parent,
    )

    # Make the request
    page_result = client.list_rule_sets(request=request)

    # Handle the response
    for response in page_result:
        print(f"Rule Sets: {response}")


# [END contentwarehouse_create_rule_set]
