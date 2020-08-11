# Copyright 2018 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import re

import batch_operation_sample


def test_batch_operation_sample(capsys):

    batch_operation_sample.run_sample()
    out, _ = capsys.readouterr()
    expected = (
        '.*Company generated:.*Company created:.*.*Job created:.*Job '
        'created:.*.*Job updated:.*Engineer in Mountain View.*Job '
        'updated:.*Engineer in Mountain View.*.*Job deleted.*Job '
        'deleted.*.*Company deleted.*')
    assert re.search(expected, out, re.DOTALL)
