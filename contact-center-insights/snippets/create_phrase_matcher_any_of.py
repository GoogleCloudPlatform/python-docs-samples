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
# [START contactcenterinsights_create_phrase_matcher_any_of]
from google.cloud import contact_center_insights_v1


def create_phrase_matcher_any_of(
    project_id: str,
) -> contact_center_insights_v1.PhraseMatcher:
    """Creates a phrase matcher that matches any of the specified queries.

    Args:
        project_id:
            The project identifier. For example, 'my-project'.

    Returns:
        A phrase matcher.
    """
    # Construct a parent resource.
    parent = (
        contact_center_insights_v1.ContactCenterInsightsClient.common_location_path(
            project_id, "us-central1"
        )
    )

    # Construct a phrase matcher that matches any of its rule groups.
    phrase_matcher = contact_center_insights_v1.PhraseMatcher()
    phrase_matcher.display_name = "PHONE_SERVICE"
    phrase_matcher.type_ = (
        contact_center_insights_v1.PhraseMatcher.PhraseMatcherType.ANY_OF
    )
    phrase_matcher.active = True

    # Construct a rule group to match the word "PHONE" or "CELLPHONE", ignoring case sensitivity.
    rule_group = contact_center_insights_v1.PhraseMatchRuleGroup()
    rule_group.type_ = (
        contact_center_insights_v1.PhraseMatchRuleGroup.PhraseMatchRuleGroupType.ANY_OF
    )

    for word in ["PHONE", "CELLPHONE"]:
        rule = contact_center_insights_v1.PhraseMatchRule()
        rule.query = word
        rule.config.exact_match_config = contact_center_insights_v1.ExactMatchConfig()
        rule_group.phrase_match_rules.append(rule)
    phrase_matcher.phrase_match_rule_groups.append(rule_group)

    # Call the Insights client to create a phrase matcher.
    insights_client = contact_center_insights_v1.ContactCenterInsightsClient()
    phrase_matcher = insights_client.create_phrase_matcher(
        parent=parent, phrase_matcher=phrase_matcher
    )

    print(f"Created {phrase_matcher.name}")
    return phrase_matcher


# [END contactcenterinsights_create_phrase_matcher_any_of]
