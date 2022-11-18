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

# [START recaptcha_enterprise_list_site_keys]
from google.cloud import recaptchaenterprise_v1
from google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service.pagers import (
    ListKeysPager,
)


def list_site_keys(project_id: str) -> ListKeysPager:
    """List all keys present under the given project ID.

    Args:
    project_id: GCloud Project ID.
    """

    project_name = f"projects/{project_id}"

    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

    # Set the project id to list the keys present in it.
    request = recaptchaenterprise_v1.ListKeysRequest()
    request.parent = project_name

    response = client.list_keys(request)
    print("Listing reCAPTCHA site keys: ")
    for i, key in enumerate(response):
        print(f"{str(i)}. {key.name}")

    return response


# [END recaptcha_enterprise_list_site_keys]


if __name__ == "__main__":
    import google.auth
    import google.auth.exceptions

    # TODO(developer): Replace the below variables before running
    try:
        default_project_id = google.auth.default()[1]
    except google.auth.exceptions.DefaultCredentialsError:
        print(
            "Please use `gcloud auth application-default login` "
            "or set GOOGLE_APPLICATION_CREDENTIALS to use this script."
        )
    else:
        list_site_keys(default_project_id)
