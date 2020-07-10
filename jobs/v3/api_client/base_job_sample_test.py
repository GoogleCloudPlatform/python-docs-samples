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

import base_job_sample


def test_base_job_sample(capsys):

    base_job_sample.run_sample()
    out, _ = capsys.readouterr()
    expected = ('.*Job generated:.*\n'
                '.*Job created:.*\n'
                '.*Job existed:.*\n'
                '.*Job updated:.*changedDescription.*\n'
                '.*Job updated:.*changedJobTitle.*\n'
                '.*Job deleted.*\n')
    assert re.search(expected, out)
