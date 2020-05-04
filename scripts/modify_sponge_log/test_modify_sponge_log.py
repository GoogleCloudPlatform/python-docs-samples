# Copyright 2020 Google, LLC
#
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

# This sample creates a secure two-service application running on Cloud Run.
# This test builds and deploys the two secure services
# to test that they interact properly together.

import filecmp
import shutil
import tempfile
from xml.etree import ElementTree

import pytest

import modify_sponge_log


@pytest.fixture(
    scope="function",
    params=[
        "test_data/no_props",
        "test_data/simplest",
        "test_data/multi_tags_with_comma",
        "test_data/multi_props",
    ])
def test_files(request):
    original_file_src = '{}/original.xml'.format(request.param)
    expected_file_src = '{}/expected.xml'.format(request.param)
    d = tempfile.TemporaryDirectory()
    original_file = '{}/original.xml'.format(d.name)
    expected_file = '{}/expected.xml'.format(d.name)
    shutil.copyfile(original_file_src, original_file)
    shutil.copyfile(expected_file_src, expected_file)

    yield original_file, expected_file

    d.cleanup()


def test_modify_sponge_log(test_files):
    original_file, expected_file = test_files

    modify_sponge_log.main(original_file)

    # Parse and rewrite the expected file with ElementTree in order to
    # use filecmp.
    expected_tree = ElementTree.parse(expected_file)
    expected_tree.write(expected_file, encoding='utf-8', xml_declaration=True)

    assert filecmp.cmp(original_file, expected_file)
