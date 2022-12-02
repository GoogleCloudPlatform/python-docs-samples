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
    output = str(subprocess.check_output("python write_user_event.py", shell=True))

    assert re.match(
        '.*write user event request.*?user_event.*?event_type: "home-page-view".*',
        output,
    )
    assert re.match('.*written user event.*?event_type: "home-page-view".*', output)
    assert re.match('.*written user event.*?visitor_id: "test_visitor_id".*', output)
