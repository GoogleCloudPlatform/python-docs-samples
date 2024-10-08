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

# [START recaptcha_enterprise_delete_site_key]
from google.cloud import recaptchaenterprise_v1


def delete_site_key(project_id: str, recaptcha_site_key: str) -> None:
    """Delete the given reCAPTCHA site key present under the project ID.

    Args:
    project_id : GCloud Project ID.
    recaptcha_site_key: Specify the key ID to be deleted.
    """

    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

    # Construct the key details.
    key_name = f"projects/{project_id}/keys/{recaptcha_site_key}"

    # Set the project ID and reCAPTCHA site key.
    request = recaptchaenterprise_v1.DeleteKeyRequest()
    request.name = key_name

    client.delete_key(request)
    print("reCAPTCHA Site key deleted successfully ! ")


# [END recaptcha_enterprise_delete_site_key]


if __name__ == "__main__":
    import google.auth
    import google.auth.exceptions

    # TODO(developer): Replace the below variables before running
    try:
        default_project_id = google.auth.default()[1]
        recaptcha_site_key = "recaptcha_site_key"
    except google.auth.exceptions.DefaultCredentialsError:
        print(
            "Please use `gcloud auth application-default login` "
            "or set GOOGLE_APPLICATION_CREDENTIALS to use this script."
        )
    else:
        delete_site_key(default_project_id, recaptcha_site_key)
