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
def test_set_inventory():
    output = str(subprocess.check_output("python set_inventory.py", shell=True))
    print(output)
    assert re.match(".*product is created.*", output)
    assert re.match(
        '.*name: "projects/.*/locations/global/catalogs/default_catalog/branches/0/products.*',
        output,
    )
    assert re.match(".*set inventory request.*", output)
    assert re.match(
        '.*get product response.*?fulfillment_info.*type_: "pickup-in-store".*?place_ids: "store1".*',
        output,
    )
    assert re.match(
        '.*get product response.*?fulfillment_info.*type_: "pickup-in-store".*?place_ids: "store2".*',
        output,
    )
    assert re.match(
        ".*product projects/.*/locations/global/catalogs/default_catalog/branches/0/products.* was deleted.*",
        output,
    )
