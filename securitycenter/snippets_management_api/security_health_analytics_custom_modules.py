#!/usr/bin/env python
#
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
import time
from typing import Dict

# [START securitycenter_get_effective_security_health_analytics_custom_module]
from google.api_core.exceptions import NotFound
from google.cloud import securitycentermanagement_v1

def get_effective_security_health_analytics_custom_module(parent: str, module_id: str):
    """
    Retrieves a Security Health Analytics custom module.
    Args:
        parent: Use any one of the following options:
                - organizations/{organization_id}/locations/{location_id}
                - folders/{folder_id}/locations/{location_id}
                - projects/{project_id}/locations/{location_id}
    Returns:
        The retrieved Security Health Analytics custom module.
    Raises:
        NotFound: If the specified custom module does not exist.
    """
    client = securitycentermanagement_v1.SecurityCenterManagementClient()

    try:
        request = securitycentermanagement_v1.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest(
            name=f"{parent}/effectiveSecurityHealthAnalyticsCustomModules/{module_id}",
        )

        response = client.get_effective_security_health_analytics_custom_module(request=request)
        print(f"Retrieved Effective Security Health Analytics Custom Module: {response.name}")
        return response
    except NotFound as e:
        print(f"Custom Module not found: {response.name}")
        raise e
# [END securitycenter_get_effective_security_health_analytics_custom_module]
