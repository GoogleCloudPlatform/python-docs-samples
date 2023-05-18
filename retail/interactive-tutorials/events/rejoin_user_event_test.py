# Copyright 2022 Google LLC
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

import re
import subprocess

from google.api_core.retry import Retry


@Retry()
def test_create_product():
    output = str(subprocess.check_output("python rejoin_user_event.py", shell=True))

    assert re.match(".*the user event is written.*", output)
    assert re.match(
        '.*rejoin user events request.*?parent: "projects/.*?/locations/global/catalogs/default_catalog.*',
        output,
    )
    assert re.match(
        ".*rejoin user events request.*?user_event_rejoin_scope: UNJOINED_EVENTS.*",
        output,
    )
    assert re.match(
        ".*the rejoin operation was started.*?projects/.*?/locations/global/catalogs/default_catalog/operations/rejoin-user-events.*",
        output,
    )
    assert re.match(
        ".*the purge operation was started.*?projects/.*?/locations/global/catalogs/default_catalog/operations/purge-user-events.*",
        output,
    )
