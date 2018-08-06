# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START functions_http_xml]
import json
# [END functions_http_xml]

# [START functions_http_xml]
import xmltodict
# [END functions_http_xml]

# [START functions_http_xml]


def parse_xml(request):
    data = xmltodict.parse(request.data)
    return json.dumps(data, indent=2)
# [END functions_http_xml]
