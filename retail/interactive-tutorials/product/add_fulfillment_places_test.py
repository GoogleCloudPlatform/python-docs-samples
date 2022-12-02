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


def test_add_fulfillment():
    output = str(
        subprocess.check_output("python add_fulfillment_places.py", shell=True)
    )

    assert re.match(".*product is created.*", output)
    assert re.match(".*add fulfillment request.*", output)
    assert re.match(".*add fulfillment places.*", output)
    assert re.match(
        '.*get product response.*?fulfillment_info.*type_: "pickup-in-store".*?place_ids: "store1".*',
        output,
    )
    assert re.match(
        '.*get product response.*?fulfillment_info.*type_: "pickup-in-store".*?place_ids: "store2".*',
        output,
    )
