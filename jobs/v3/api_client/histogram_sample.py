#!/usr/bin/env python

# Copyright 2018 Google LLC All Rights Reserved.
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

# [START instantiate]
import os
import time

from googleapiclient.discovery import build

client_service = build('jobs', 'v3')
parent = 'projects/' + os.environ['GOOGLE_CLOUD_PROJECT']
# [END instantiate]


# [START histogram_search]
def histogram_search(client_service, company_name):
    request_metadata = {
        'user_id': 'HashedUserId',
        'session_id': 'HashedSessionId',
        'domain': 'www.google.com'
    }
    custom_attribute_histogram_facet = {
        'key': 'someFieldName1',
        'string_value_histogram': True
    }
    histogram_facets = {
        'simple_histogram_facets': ['COMPANY_ID'],
        'custom_attribute_histogram_facets': [custom_attribute_histogram_facet]
    }
    request = {
        'search_mode': 'JOB_SEARCH',
        'request_metadata': request_metadata,
        'histogram_facets': histogram_facets
    }
    if company_name is not None:
        request.update({'job_query': {'company_names': [company_name]}})
    response = client_service.projects().jobs().search(
        parent=parent, body=request).execute()
    print(response)
# [END histogram_search]


def set_up():
    import base_company_sample
    import base_job_sample
    import custom_attribute_sample as caa

    company_to_be_created = base_company_sample.generate_company()
    company_created = base_company_sample.create_company(
        client_service, company_to_be_created)
    company_name = company_created.get('name')

    job_to_be_created = caa.generate_job_with_custom_attributes(company_name)
    job_name = base_job_sample.create_job(client_service,
                                          job_to_be_created).get('name')
    return company_name, job_name


def tear_down(company_name, job_name):
    import base_company_sample
    import base_job_sample

    base_job_sample.delete_job(client_service, job_name)
    base_company_sample.delete_company(client_service, company_name)


def run_sample(company_name):
    histogram_search(client_service, company_name)


if __name__ == '__main__':
    company_name, job_name = set_up()
    # Wait several seconds for post processing
    time.sleep(10)
    run_sample(company_name)
    tear_down(company_name, job_name)
