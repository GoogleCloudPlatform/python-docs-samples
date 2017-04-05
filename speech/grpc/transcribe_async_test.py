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

from transcribe_async import main

BUCKET = os.environ['CLOUD_STORAGE_BUCKET']


def test_main(capsys):
    # Run the transcribe sample on audio.raw, verify correct results
    storage_uri = 'gs://{}/speech/audio.raw'.format(BUCKET)
    main(storage_uri, 'LINEAR16', 16000)
    out, err = capsys.readouterr()
    assert re.search(r'how old is the Brooklyn Bridge', out, re.DOTALL | re.I)
