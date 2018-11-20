#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
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

import time

# [START instantiate]
from googleapiclient.discovery import build

client_service = build('jobs', 'v2')
# [END instantiate]


# [START basic_location_search]
def basic_location_search(client_service, company_name, location, distance):
    request_metadata = {
        'user_id': 'HashedUserId',
        'session_id': 'HashedSessionId',
        'domain': 'www.google.com'
    }
    location_filter = {'name': location, 'distance_in_miles': distance}
    job_query = {'location_filters': [location_filter]}
    if company_name is not None:
        job_query.update({'company_names': [company_name]})
    request = {
        'query': job_query,
        'request_metadata': request_metadata,
        'mode': 'JOB_SEARCH',
    }
    response = client_service.jobs().search(body=request).execute()
    print(response)
# [END basic_location_search]


# [START keyword_location_search]
def keyword_location_search(client_service, company_name, location, distance,
                            keyword):
    request_metadata = {
        'user_id': 'HashedUserId',
        'session_id': 'HashedSessionId',
        'domain': 'www.google.com'
    }
    location_filter = {'name': location, 'distance_in_miles': distance}
    job_query = {'location_filters': [location_filter], 'query': keyword}
    if company_name is not None:
        job_query.update({'company_names': [company_name]})
    request = {
        'query': job_query,
        'request_metadata': request_metadata,
        'mode': 'JOB_SEARCH',
    }
    response = client_service.jobs().search(body=request).execute()
    print(response)
# [END keyword_location_search]


# [START city_location_search]
def city_location_search(client_service, company_name, location):
    request_metadata = {
        'user_id': 'HashedUserId',
        'session_id': 'HashedSessionId',
        'domain': 'www.google.com'
    }
    location_filter = {'name': location}
    job_query = {'location_filters': [location_filter]}
    if company_name is not None:
        job_query.update({'company_names': [company_name]})
    request = {
        'query': job_query,
        'request_metadata': request_metadata,
        'mode': 'JOB_SEARCH',
    }
    response = client_service.jobs().search(body=request).execute()
    print(response)
# [END city_location_search]


# [START multi_locations_search]
def multi_locations_search(client_service, company_name, location1, distance1,
                           location2):
    request_metadata = {
        'user_id': 'HashedUserId',
        'session_id': 'HashedSessionId',
        'domain': 'www.google.com'
    }
    location_filter1 = {'name': location1, 'distance_in_miles': distance1}
    location_filter2 = {'name': location2}
    job_query = {'location_filters': [location_filter1, location_filter2]}
    if company_name is not None:
        job_query.update({'company_names': [company_name]})
    request = {
        'query': job_query,
        'request_metadata': request_metadata,
        'mode': 'JOB_SEARCH',
    }
    response = client_service.jobs().search(body=request).execute()
    print(response)
# [END multi_locations_search]


# [START broadening_location_search]
def broadening_location_search(client_service, company_name, location):
    request_metadata = {
        'user_id': 'HashedUserId',
        'session_id': 'HashedSessionId',
        'domain': 'www.google.com'
    }
    location_filter = {'name': location}
    job_query = {'location_filters': [location_filter]}
    if company_name is not None:
        job_query.update({'company_names': [company_name]})
    request = {
        'query': job_query,
        'request_metadata': request_metadata,
        'mode': 'JOB_SEARCH',
        'enable_broadening': True
    }
    response = client_service.jobs().search(body=request).execute()
    print(response)
# [END broadening_location_search]


def run_sample():
    import base_company_sample
    import base_job_sample

    company_to_be_created = base_company_sample.generate_company()
    company_created = base_company_sample.create_company(
        client_service, company_to_be_created)
    company_name = company_created.get('name')

    location = 'Mountain View, CA'
    distance = 0.5
    keyword = 'Software Engineer'
    location2 = 'Synnyvale, CA'

    job_to_be_created = base_job_sample.generate_job_with_required_fields(
        company_name)
    job_to_be_created.update({'locations': [location], 'job_title': keyword})
    job_name = base_job_sample.create_job(client_service,
                                          job_to_be_created).get('name')

    job_to_be_created2 = base_job_sample.generate_job_with_required_fields(
        company_name)
    job_to_be_created2.update({'locations': [location2], 'job_title': keyword})
    job_name2 = base_job_sample.create_job(client_service,
                                           job_to_be_created2).get('name')

    # Wait several seconds for post processing
    time.sleep(10)
    basic_location_search(client_service, company_name, location, distance)
    city_location_search(client_service, company_name, location)
    broadening_location_search(client_service, company_name, location)
    keyword_location_search(client_service, company_name, location, distance,
                            keyword)
    multi_locations_search(client_service, company_name, location, distance,
                           location2)

    base_job_sample.delete_job(client_service, job_name)
    base_job_sample.delete_job(client_service, job_name2)
    base_company_sample.delete_company(client_service, company_name)


if __name__ == '__main__':
    run_sample()
