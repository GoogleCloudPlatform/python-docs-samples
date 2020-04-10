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
import uuid

from flaky import flaky

from create_instance import main

PROJECT = os.environ['GCLOUD_PROJECT']
BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
INSTANCE_NAME = 'test-instance-' + str(uuid.uuid4())


@flaky
def test_main(capsys):
    main(
        PROJECT,
        BUCKET,
        'us-central1-f',
        INSTANCE_NAME,
        wait=False)

    out, _ = capsys.readouterr()

    assert "Instances in project" in out
    assert "zone us-central1-f" in out
    assert INSTANCE_NAME in out
    assert "Deleting instance" in out
