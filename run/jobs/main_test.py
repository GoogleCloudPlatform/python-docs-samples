# Copyright 2020 Google, LLC.
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

import os

import pytest

import main

def test_main(capsys):
    main.main()
    out, _ = capsys.readouterr()
    expected = f"Completed Task #0."
    assert expected in out


def test_env_vars(capsys):
    # os.setenv['FAIL_RATE'] = 0.9
    main.main()
    out, _ = capsys.readouterr()
    expected = f"Completed Task #0."
    assert expected in out