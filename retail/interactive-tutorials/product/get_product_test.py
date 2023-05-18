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
def test_get_product():
    output = str(subprocess.check_output("python get_product.py", shell=True))

    assert re.match(".*get product request.*", output)
    assert re.match(".*get product response.*", output)
    assert re.match(
        ".*get product response.*?name.*?projects/.*/locations/global/catalogs/default_catalog/branches/0/products/.*",
        output,
    )
    assert re.match(".*get product response.*?title.*?Nest Mini.*", output)
    assert re.match(".*product.*was deleted.*", output)
