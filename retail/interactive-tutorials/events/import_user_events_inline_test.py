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


def test_create_product():
    output = str(
        subprocess.check_output("python import_user_events_inline.py", shell=True)
    )

    assert re.match(
        '.*import user events from inline source request.*?parent: "projects/.*?/locations/global/catalogs/default_catalog.*',
        output,
    )
    assert re.match(
        ".*import user events from inline source request.*?input_config.*?user_event_inline_source.*",
        output,
    )
    assert re.match(
        ".*the operation was started.*?projects/.*?/locations/global/catalogs/default_catalog/operations/import-user-events.*",
        output,
    )
    assert re.match(".*import user events operation is done.*", output)
    assert re.match(".*number of successfully imported events.*?3.*", output)
    assert re.match(".*number of failures during the importing.*?0.*", output)
