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


def create_model_armor_template(project_id: str, location: str, template_id: str) -> Template:
    # [START modelarmor_create_template]

    from google.api_core.client_options import ClientOptions
    from google.cloud.modelarmor_v1 import (
        Template,
        DetectionConfidenceLevel,
        FilterConfig,
        PiAndJailbreakFilterSettings,
        MaliciousUriFilterSettings,
        ModelArmorClient,
        CreateTemplateRequest
    )

    client = ModelArmorClient(
        transport="rest",
        client_options=ClientOptions(api_endpoint=f"modelarmor.{location}.rep.googleapis.com"),
    )

    # TODO(Developer): Uncomment these variables and initialize
    # project_id = "your-google-cloud-project-id"
    # location = "us-central1"
    # template_id = "template_id"

    template = Template(
        filter_config=FilterConfig(
            pi_and_jailbreak_filter_settings=PiAndJailbreakFilterSettings(
                filter_enforcement=PiAndJailbreakFilterSettings.PiAndJailbreakFilterEnforcement.ENABLED,
                confidence_level=DetectionConfidenceLevel.MEDIUM_AND_ABOVE,
            ),
            malicious_uri_filter_settings=MaliciousUriFilterSettings(
                filter_enforcement=MaliciousUriFilterSettings.MaliciousUriFilterEnforcement.ENABLED,
            )
        ),
    )

    # Initialize request arguments
    request = CreateTemplateRequest(
        parent=f"projects/{project_id}/locations/{location}",
        template_id=template_id,
        template=template,
    )

    # Make the request
    response = client.create_template(request=request)
    # Response
    print(response.name)

# [END modelarmor_create_template]

    return response
