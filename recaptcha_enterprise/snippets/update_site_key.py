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

# [START recaptcha_enterprise_update_site_key]
import time

from google.cloud import recaptchaenterprise_v1


def update_site_key(project_id: str, recaptcha_site_key: str, domain_name: str) -> None:
    """
    Update the properties of the given site key present under the project id.

    Args:
    project_id: GCloud Project ID.
    recaptcha_site_key: Specify the site key.
    domain_name: Specify the domain name for which the settings should be updated.
    """

    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

    # Construct the key details.
    key_name = f"projects/{project_id}/keys/{recaptcha_site_key}"

    # Set the name and the new settings for the key.
    web_settings = recaptchaenterprise_v1.WebKeySettings()
    web_settings.allow_amp_traffic = True
    web_settings.allowed_domains.append(domain_name)

    key = recaptchaenterprise_v1.Key()
    key.display_name = "any descriptive name for the key"
    key.name = key_name
    key.web_settings = web_settings

    update_key_request = recaptchaenterprise_v1.UpdateKeyRequest()
    update_key_request.key = key
    client.update_key(update_key_request)

    time.sleep(5)

    # Retrieve the key and check if the property is updated.
    get_key_request = recaptchaenterprise_v1.GetKeyRequest()
    get_key_request.name = key_name
    response = client.get_key(get_key_request)
    web_settings = response.web_settings

    # Get the changed property.
    if not web_settings.allow_amp_traffic:
        print(
            "Error! reCAPTCHA Site key property hasn't been updated. Please try again !"
        )
    else:
        print("reCAPTCHA Site key successfully updated ! ")


# [END recaptcha_enterprise_update_site_key]


if __name__ == "__main__":
    import google.auth
    import google.auth.exceptions

    # TODO(developer): Replace the below variables before running
    try:
        default_project_id = google.auth.default()[1]
        recaptcha_site_key = "recaptcha_site_key"
        domain_name = "localhost"
    except google.auth.exceptions.DefaultCredentialsError:
        print(
            "Please use `gcloud auth application-default login` "
            "or set GOOGLE_APPLICATION_CREDENTIALS to use this script."
        )
    else:
        update_site_key(default_project_id, recaptcha_site_key, domain_name)
