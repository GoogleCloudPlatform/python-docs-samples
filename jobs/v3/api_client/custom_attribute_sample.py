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
import random
import string
import time

from googleapiclient.discovery import build

client_service = build('jobs', 'v3')
parent = 'projects/' + os.environ['GOOGLE_CLOUD_PROJECT']
# [END instantiate]


# [START custom_attribute_job]
def generate_job_with_custom_attributes(company_name):
    # Requisition id should be a unique Id in your system.
    requisition_id = 'job_with_custom_attributes:' + ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(16))

    job_title = 'Software Engineer'
    application_urls = ['http://careers.google.com']
    description = ('Design, develop, test, deploy, maintain and improve '
                   'software.')

    custom_attributes = {
        'someFieldName1': {
            'string_values': ['value1'],
            'filterable': True
        },
        'someFieldName2': {
            'long_values': [256],
            'filterable': True
        }
    }

    job = {
        'company_name': company_name,
        'requisition_id': requisition_id,
        'title': job_title,
        'application_info': {'uris': application_urls},
        'description': description,
        'custom_attributes': custom_attributes
    }
    print('Job generated: %s' % job)
    return job
# [END custom_attribute_job]


# [START custom_attribute_filter_string_value]
def custom_attribute_filter_string_value(client_service):
    request_metadata = {
        'user_id': 'HashedUserId',
        'session_id': 'HashedSessionId',
        'domain': 'www.google.com'
    }

    custom_attribute_filter = 'NOT EMPTY(someFieldName1)'
    job_query = {'custom_attribute_filter': custom_attribute_filter}
    request = {
        'request_metadata': request_metadata,
        'job_query': job_query,
        'job_view': 'JOB_VIEW_FULL'
    }

    response = client_service.projects().jobs().search(
        parent=parent, body=request).execute()
    print(response)
# [END custom_attribute_filter_string_value]


# [START custom_attribute_filter_long_value]
def custom_attribute_filter_long_value(client_service):
    request_metadata = {
        'user_id': 'HashedUserId',
        'session_id': 'HashedSessionId',
        'domain': 'www.google.com'
    }

    custom_attribute_filter = ('(255 <= someFieldName2) AND'
                               ' (someFieldName2 <= 257)')
    job_query = {'custom_attribute_filter': custom_attribute_filter}
    request = {
        'request_metadata': request_metadata,
        'job_query': job_query,
        'job_view': 'JOB_VIEW_FULL'
    }

    response = client_service.projects().jobs().search(
        parent=parent, body=request).execute()
    print(response)
# [END custom_attribute_filter_long_value]


# [START custom_attribute_filter_multi_attributes]
def custom_attribute_filter_multi_attributes(client_service):
    request_metadata = {
        'user_id': 'HashedUserId',
        'session_id': 'HashedSessionId',
        'domain': 'www.google.com'
    }

    custom_attribute_filter = (
        '(someFieldName1 = "value1") AND ((255 <= someFieldName2) OR '
        '(someFieldName2 <= 213))')
    job_query = {'custom_attribute_filter': custom_attribute_filter}
    request = {
        'request_metadata': request_metadata,
        'job_query': job_query,
        'job_view': 'JOB_VIEW_FULL'
    }

    response = client_service.projects().jobs().search(
        parent=parent, body=request).execute()
    print(response)
# [END custom_attribute_filter_multi_attributes]


def set_up():
    import base_company_sample
    import base_job_sample

    company_to_be_created = base_company_sample.generate_company()
    company_created = base_company_sample.create_company(
        client_service, company_to_be_created)
    company_name = company_created.get('name')

    job_to_be_created = generate_job_with_custom_attributes(company_name)
    job_name = base_job_sample.create_job(client_service,
                                          job_to_be_created).get('name')
    return company_name, job_name


def tear_down(company_name, job_name):
    import base_company_sample
    import base_job_sample
    base_job_sample.delete_job(client_service, job_name)
    base_company_sample.delete_company(client_service, company_name)


def run_sample():
    custom_attribute_filter_string_value(client_service)
    custom_attribute_filter_long_value(client_service)
    custom_attribute_filter_multi_attributes(client_service)


if __name__ == '__main__':
    company_name, job_name = set_up()
    # Wait several seconds for post processing
    time.sleep(10)
    run_sample(company_name, job_name)
