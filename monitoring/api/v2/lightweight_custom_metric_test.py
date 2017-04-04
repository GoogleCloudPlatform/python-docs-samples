#!/usr/bin/env python

# Copyright 2015 Google Inc. All rights reserved.
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

import os
import re

import lightweight_custom_metric

PROJECT = os.environ['GCLOUD_PROJECT']


def test_main(capsys):
    lightweight_custom_metric.main(PROJECT)
    output, _ = capsys.readouterr()

    assert re.search(
        re.compile(
            r'Point:\s*'),
        output)
