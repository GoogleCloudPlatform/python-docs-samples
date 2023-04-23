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

import json
import os
from typing import Dict

from middleware import logger


# [START cloudrun_user_auth_secrets]
def get_cred_config() -> dict[str, str]:
    secret = os.environ.get("CLOUD_SQL_CREDENTIALS_SECRET")
    if secret:
        return json.loads(secret)
    # [END cloudrun_user_auth_secrets]
    else:
        logger.info(
            "CLOUD_SQL_CREDENTIALS_SECRET env var not set. Defaulting to environment variables."
        )
        if "DB_USER" not in os.environ:
            raise Exception("DB_USER needs to be set.")

        if "DB_PASSWORD" not in os.environ:
            raise Exception("DB_PASSWORD needs to be set.")

        if "DB_NAME" not in os.environ:
            raise Exception("DB_NAME needs to be set.")

        if "CLOUD_SQL_CONNECTION_NAME" not in os.environ:
            raise Exception("CLOUD_SQL_CONNECTION_NAME needs to be set.")

        return {
            "DB_USER": os.environ["DB_USER"],
            "DB_PASSWORD": os.environ["DB_PASSWORD"],
            "DB_NAME": os.environ["DB_NAME"],
            "DB_HOST": os.environ.get("DB_HOST", None),
            "CLOUD_SQL_CONNECTION_NAME": os.environ["CLOUD_SQL_CONNECTION_NAME"],
        }
