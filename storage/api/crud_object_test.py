# Copyright 2016, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

from crud_object import main


def test_main(cloud_config, capsys):
    main(cloud_config.storage_bucket, __file__)
    out, err = capsys.readouterr()

    assert not re.search(r'Downloaded file [!]=', out)
    assert re.search(r'Uploading.*Fetching.*Deleting.*Done', out, re.DOTALL)
