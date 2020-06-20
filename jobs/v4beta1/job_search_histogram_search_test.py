# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import job_search_histogram_search

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


def test_search_jobs_histogram(tenant):
    query = "count(base_compensation, [bucket(12, 20)])"
    jobs = job_search_histogram_search.search_jobs(PROJECT_ID, tenant, query)
    for job in jobs:
        assert "projects/" in job
