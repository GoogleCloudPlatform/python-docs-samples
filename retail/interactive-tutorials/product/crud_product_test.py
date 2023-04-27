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
def test_add_fulfillment():
    output = str(subprocess.check_output("python crud_product.py", shell=True))

    assert re.match(".*create product request.*", output)
    assert re.match(".*create product request.*", output)
    assert re.match('.*create product request.*?title: "Nest Mini".*', output)
    assert re.match(".*created product.*", output)
    assert re.match('.*created product.*?title: "Nest Mini".*', output)

    assert re.match(".*get product request.*", output)
    assert re.match(".*get product response.*", output)

    assert re.match(".*update product request.*", output)
    assert re.match('.*update product request.*?title: "Updated Nest Mini.*', output)
    assert re.match(".*updated product.*?title.*?Updated Nest Mini.*", output)
    assert re.match(".*updated product.*?brands.*?Updated Google.*", output)
    assert re.match(".*updated product.*?price.*?20.*", output)
    assert re.match(".*product was deleted.*", output)
