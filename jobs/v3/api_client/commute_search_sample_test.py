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

import backoff
from googleapiclient.errors import HttpError
import pytest

import commute_search_sample


@pytest.fixture(scope="module")
def company_name():
    company_name, job_name = commute_search_sample.set_up()
    yield company_name
    commute_search_sample.tear_down(company_name, job_name)


def test_commute_search_sample(company_name, capsys):
    @backoff.on_exception(backoff.expo, (AssertionError, HttpError), max_time=240)
    def eventually_consistent_test():
        commute_search_sample.run_sample(company_name)
        out, _ = capsys.readouterr()
        expected = ('.*matchingJobs.*1600 Amphitheatre Pkwy.*')
        assert re.search(expected, out)

    eventually_consistent_test()
