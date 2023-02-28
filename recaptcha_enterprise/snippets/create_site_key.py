#!/usr/bin/env python
# Copyright 2021 Google, Inc
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
#
# All Rights Reserved.

# [START recaptcha_enterprise_create_site_key]
from google.cloud import recaptchaenterprise_v1


def create_site_key(project_id: str, domain_name: str) -> str:
    """Create reCAPTCHA Site key which binds a domain name to a unique key.
    Args:
    project_id : GCloud Project ID.
    domain_name: Specify the domain name in which the reCAPTCHA should be activated.
    """
    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

    # Set the type of the reCAPTCHA to be displayed.
    # For different types, see: https://cloud.google.com/recaptcha-enterprise/docs/keys
    web_settings = recaptchaenterprise_v1.WebKeySettings()
    web_settings.allowed_domains.append(domain_name)
    web_settings.allow_amp_traffic = False
    web_settings.integration_type = web_settings.IntegrationType.SCORE

    key = recaptchaenterprise_v1.Key()
    key.display_name = "any descriptive name for the key"
    key.web_settings = web_settings

    # Create the request.
    request = recaptchaenterprise_v1.CreateKeyRequest()
    request.parent = f"projects/{project_id}"
    request.key = key

    # Get the name of the created reCAPTCHA site key.
    response = client.create_key(request)
    recaptcha_site_key = response.name.rsplit("/", maxsplit=1)[1]
    print("reCAPTCHA Site key created successfully. Site Key: " + recaptcha_site_key)
    return recaptcha_site_key


# [END recaptcha_enterprise_create_site_key]

if __name__ == "__main__":
    import google.auth
    import google.auth.exceptions

    # TODO(developer): Replace the below variables before running
    try:
        default_project_id = google.auth.default()[1]
        domain_name = "localhost"
    except google.auth.exceptions.DefaultCredentialsError:
        print(
            "Please use `gcloud auth application-default login` "
            "or set GOOGLE_APPLICATION_CREDENTIALS to use this script."
        )
    else:
        create_site_key(default_project_id, domain_name)
