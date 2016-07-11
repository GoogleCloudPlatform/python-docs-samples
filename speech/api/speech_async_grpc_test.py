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

import argparse
import re
import sys

import pytest
from speech_async_grpc import _gcs_uri
from speech_async_grpc import main


@pytest.mark.skipif(
        sys.version_info >= (3, 0),
        reason=("grpc doesn't yet support python3 "
                'https://github.com/grpc/grpc/issues/282'))
def test_main(cloud_config, capsys):
    input_uri = 'gs://{}/speech/audio.flac'.format(cloud_config.storage_bucket)

    main(input_uri, 'FLAC', 16000)

    out, err = capsys.readouterr()
    assert re.search(r'how old is the Brooklyn Bridge', out, re.DOTALL | re.I)


def test_gcs_uri():
    _gcs_uri('gs://bucket/path')
    with pytest.raises(argparse.ArgumentTypeError):
        _gcs_uri('/local/path')
