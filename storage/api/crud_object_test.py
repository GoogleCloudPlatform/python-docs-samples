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

import os
import re
import tempfile

import pytest

from crud_object import main


BUCKET = os.environ['CLOUD_STORAGE_BUCKET']


@pytest.fixture()
def test_file():
    _, file_path = tempfile.mkstemp()

    with open(file_path, "w+b") as f:
        f.write(b"hello world")

    yield file_path

    os.remove(file_path)


def test_main(capsys, test_file):
    main(BUCKET, test_file)
    out, err = capsys.readouterr()

    assert not re.search(r'Downloaded file [!]=', out)
    assert re.search(r'Uploading.*Fetching.*Deleting.*Done', out, re.DOTALL)
