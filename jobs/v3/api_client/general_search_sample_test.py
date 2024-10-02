# Copyright 2018 Google LLC.
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
import pytest

import general_search_sample


@pytest.fixture(scope="module")
def company_and_job():
    company_name, job_name = general_search_sample.set_up()
    yield company_name, job_name
    general_search_sample.tear_down(company_name, job_name)


@pytest.mark.flaky(max_runs=2, min_passes=1)
def test_general_search_sample(company_and_job, capsys):
    @backoff.on_exception(backoff.expo, AssertionError, max_time=120)
    def eventually_consistent_test():
        general_search_sample.run_sample(company_and_job[0], company_and_job[1])
        out, _ = capsys.readouterr()
        expected = (
            ".*matchingJobs.*\n"
            ".*matchingJobs.*\n"
            ".*matchingJobs.*\n"
            ".*matchingJobs.*\n"
            ".*matchingJobs.*\n"
            ".*matchingJobs.*\n"
            ".*matchingJobs.*\n"
        )
        assert re.search(expected, out, re.DOTALL)

    eventually_consistent_test()
