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
import pytest

import custom_attribute_sample


@pytest.fixture(scope="module")
def create_data():
    company_name, job_name = custom_attribute_sample.set_up()
    yield
    custom_attribute_sample.tear_down(company_name, job_name)


@pytest.mark.flaky(min_passes=1, max_runs=3)
def test_custom_attribute_sample(create_data, capsys):
    @backoff.on_exception(backoff.expo, AssertionError, max_time=120)
    def eventually_consistent_test():
        custom_attribute_sample.run_sample()
        out, _ = capsys.readouterr()
        expected = ('.*matchingJobs.*job_with_custom_attributes.*\n'
                    '.*matchingJobs.*job_with_custom_attributes.*\n'
                    '.*matchingJobs.*job_with_custom_attributes.*\n')
        assert re.search(expected, out, re.DOTALL)

    eventually_consistent_test()
