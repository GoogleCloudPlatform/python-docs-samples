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

from compose_objects import main

RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')
BUCKET = os.environ['CLOUD_STORAGE_BUCKET']


def test_main():
    main(
        BUCKET,
        'dest.txt',
        [os.path.join(RESOURCES, 'file1.txt'),
         os.path.join(RESOURCES, 'file2.txt')]
    )
