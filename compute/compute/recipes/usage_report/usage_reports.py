#  Copyright 2022 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# flake8: noqa
"""
A sample script showing how to handle default values when communicating
with the Compute Engine API and how to configure usage reports using the API.
"""
# <REGION compute_instances_verify_default_value>
# <REGION compute_usage_report_set>
# <REGION compute_usage_report_get>
# <REGION compute_usage_report_disable>
# <IMPORTS/>

# </REGION compute_usage_report_disable>
# </REGION compute_usage_report_get>
# </REGION compute_usage_report_set>


# <REGION compute_usage_report_set>

# <INGREDIENT wait_for_extended_operation />

# <INGREDIENT set_usage_export_bucket />

# </REGION compute_usage_report_set>

# <REGION compute_usage_report_get>
# <INGREDIENT get_usage_export_bucket />

# </REGION compute_usage_report_get>
# </REGION compute_instances_verify_default_value>


# <REGION compute_usage_report_disable>

# <INGREDIENT wait_for_extended_operation />

# <INGREDIENT disable_usage_export />

# </REGION compute_usage_report_disable>
