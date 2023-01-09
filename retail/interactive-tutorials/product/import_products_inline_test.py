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


def test_import_products_gcs():
    output = str(
        subprocess.check_output("python import_products_inline_source.py", shell=True)
    )

    assert re.match(".*import products from inline source request.*", output)
    assert re.match(".*the operation was started.*", output)
    assert re.match(
        ".*projects/.*/locations/global/catalogs/default_catalog/branches/0/operations/import-products.*",
        output,
    )

    assert re.match(".*number of successfully imported products.*?2.*", output)
    assert re.match(".*number of failures during the importing.*?0.*", output)
