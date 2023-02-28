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

# [START recaptcha_enterprise_migrate_site_key]
from google.cloud import recaptchaenterprise_v1

from list_site_keys import list_site_keys


def migrate_site_key(project_id: str, recaptcha_site_key: str) -> None:
    """Migrate a key from reCAPTCHA (non-Enterprise) to reCAPTCHA Enterprise.
        If you created the key using Admin console: https://www.google.com/recaptcha/admin/site,
        then use this API to migrate to reCAPTCHA Enterprise.
        For more info, see: https://cloud.google.com/recaptcha-enterprise/docs/migrate-recaptcha
    Args:
    project_id: Google Cloud Project ID.
    recaptcha_site_key: Specify the site key to migrate.
    """

    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

    # Specify the key name to migrate.
    name = f"projects/{project_id}/keys/{recaptcha_site_key}"
    request = recaptchaenterprise_v1.MigrateKeyRequest()
    request.name = name

    response = client.migrate_key(request)
    # To verify if the site key has been migrated, use 'list_site_keys' to check if the
    # key is present.
    for key in list_site_keys(project_id):
        if key.name == response.name:
            print(f"Key migrated successfully: {recaptcha_site_key}")


# [END recaptcha_enterprise_migrate_site_key]
