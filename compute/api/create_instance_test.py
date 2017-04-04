# Copyright 2015, Google, Inc.
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

from gcp.testing.flaky import flaky

from create_instance import main

PROJECT = os.environ['GCLOUD_PROJECT']
BUCKET = os.environ['CLOUD_STORAGE_BUCKET']


@flaky
def test_main(capsys):
    main(
        PROJECT,
        BUCKET,
        'us-central1-f',
        'test-instance',
        wait=False)

    out, _ = capsys.readouterr()

    expected_output = re.compile(
        (r'Instances in project .* and zone us-central1-.* - test-instance'
         r'.*Deleting instance.*done..$'),
        re.DOTALL)

    assert re.search(expected_output, out)
