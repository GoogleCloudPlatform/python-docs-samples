# Copyright 2025 Google LLC
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

from google.cloud.modelarmor_v1 import Template


def update_model_armor_template(project_id: str, location: str, template_id: str) -> Template:
    # [START modelarmor_update_template]

    from google.api_core.client_options import ClientOptions
    from google.cloud.modelarmor_v1 import (
        Template,
        DetectionConfidenceLevel,
        FilterConfig,
        PiAndJailbreakFilterSettings,
        MaliciousUriFilterSettings,
        ModelArmorClient,
        UpdateTemplateRequest
    )

    client = ModelArmorClient(
        transport="rest",
        client_options=ClientOptions(api_endpoint=f"modelarmor.{location}.rep.googleapis.com"),
    )

    # TODO(Developer): Uncomment these variables and initialize
    # project_id = "YOUR_PROJECT_ID"
    # location = "us-central1"
    # template_id = "template_id"

    updated_template = Template(
        name=f"projects/{project_id}/locations/{location}/templates/{template_id}",
        filter_config=FilterConfig(
            pi_and_jailbreak_filter_settings=PiAndJailbreakFilterSettings(
                filter_enforcement=PiAndJailbreakFilterSettings.PiAndJailbreakFilterEnforcement.ENABLED,
                confidence_level=DetectionConfidenceLevel.LOW_AND_ABOVE,
            ),
            malicious_uri_filter_settings=MaliciousUriFilterSettings(
                filter_enforcement=MaliciousUriFilterSettings.MaliciousUriFilterEnforcement.ENABLED,
            )
        ),
    )

    # Initialize request argument(s)
    request = UpdateTemplateRequest(template=updated_template)

    # Make the request
    response = client.update_template(request=request)
    # Print the updated config
    print(response.filter_config)

# [END modelarmor_update_template]

    # Response
    return response
