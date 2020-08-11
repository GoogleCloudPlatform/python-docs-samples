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


# [START commute_search]
def commute_search(client_service, company_name):
    request_metadata = {
        'user_id': 'HashedUserId',
        'session_id': 'HashedSessionId',
        'domain': 'www.google.com'
    }
    start_location = {'latitude': 37.422408, 'longitude': -122.085609}
    commute_preference = {
        'road_traffic': 'TRAFFIC_FREE',
        'commute_method': 'TRANSIT',
        'travel_duration': '1000s',
        'start_coordinates': start_location
    }
    job_query = {'commute_filter': commute_preference}
    if company_name is not None:
        job_query.update({'company_names': [company_name]})
    request = {
        'job_query': job_query,
        'request_metadata': request_metadata,
        'job_view': 'JOB_VIEW_FULL',
        'require_precise_result_size': True
    }
    response = client_service.projects().jobs().search(
        parent=parent, body=request).execute()
    print(response)
# [END commute_search]


def set_up():
    import base_company_sample
    import base_job_sample

    company_to_be_created = base_company_sample.generate_company()
    company_created = base_company_sample.create_company(
        client_service, company_to_be_created)
    company_name = company_created.get('name')

    job_to_be_created = base_job_sample.generate_job_with_required_fields(
        company_name)
    job_to_be_created.update({
        'addresses': ['1600 Amphitheatre Pkwy, Mountain View, CA 94043']
    })
    job_name = base_job_sample.create_job(client_service,
                                          job_to_be_created).get('name')
    return company_name, job_name


def tear_down(company_name, job_name):
    import base_company_sample
    import base_job_sample

    base_job_sample.delete_job(client_service, job_name)
    base_company_sample.delete_company(client_service, company_name)


def run_sample(company_name):
    commute_search(client_service, company_name)


if __name__ == '__main__':
    company_name, job_name = set_up()
    # Wait several seconds for post processing
    time.sleep(10)
    run_sample(company_name)
    tear_down(company_name, job_name)
