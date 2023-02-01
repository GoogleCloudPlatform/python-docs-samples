# Copyright 2017 Google LLC
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

import backoff

import quickstart


PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]


def test_quickstart(capsys):
    @backoff.on_exception(backoff.expo, AssertionError, max_time=60)
    def eventually_consistent_test():
        quickstart.run_quickstart(PROJECT)
        out, _ = capsys.readouterr()
        assert "wrote" in out

    eventually_consistent_test()
