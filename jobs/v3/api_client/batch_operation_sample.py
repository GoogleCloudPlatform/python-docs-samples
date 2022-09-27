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

from googleapiclient.discovery import build

client_service = build('jobs', 'v3')
parent = 'projects/' + os.environ['GOOGLE_CLOUD_PROJECT']
# [END instantiate]


# [START job_discovery_batch_job_create]
def batch_job_create(client_service, company_name):
    import base_job_sample
    created_jobs = []

    def job_create_callback(request_id, response, exception):
        if exception is not None:
            print('Got exception while creating job: %s' % exception)
            pass
        else:
            print('Job created: %s' % response)
            created_jobs.append(response)
            pass

    batch = client_service.new_batch_http_request()
    job_to_be_created1 = base_job_sample.generate_job_with_required_fields(
        company_name)
    request1 = {'job': job_to_be_created1}
    batch.add(
        client_service.projects().jobs().create(parent=parent, body=request1),
        callback=job_create_callback)

    job_to_be_created2 = base_job_sample.generate_job_with_required_fields(
        company_name)
    request2 = {'job': job_to_be_created2}
    batch.add(
        client_service.projects().jobs().create(parent=parent, body=request2),
        callback=job_create_callback)
    batch.execute()

    return created_jobs
# [END job_discovery_batch_job_create]


# [START job_discovery_batch_job_update]
def batch_job_update(client_service, jobs_to_be_updated):
    updated_jobs = []

    def job_update_callback(request_id, response, exception):
        if exception is not None:
            print('Got exception while updating job: %s' % exception)
            pass
        else:
            print('Job updated: %s' % response)
            updated_jobs.append(response)
            pass

    batch = client_service.new_batch_http_request()
    for index in range(0, len(jobs_to_be_updated)):
        job_to_be_updated = jobs_to_be_updated[index]
        job_to_be_updated.update({'title': 'Engineer in Mountain View'})
        request = {'job': job_to_be_updated}
        if index % 2 == 0:
            batch.add(
                client_service.projects().jobs().patch(
                    name=job_to_be_updated.get('name'), body=request),
                callback=job_update_callback)
        else:
            request.update({'update_mask': 'title'})
            batch.add(
                client_service.projects().jobs().patch(
                    name=job_to_be_updated.get('name'), body=request),
                callback=job_update_callback)

    batch.execute()

    return updated_jobs
# [END job_discovery_batch_job_update]


# [START job_discovery_batch_job_delete]
def batch_job_delete(client_service, jobs_to_be_deleted):

    def job_delete_callback(request_id, response, exception):
        if exception is not None:
            print('Got exception while deleting job: %s' % exception)
            pass
        else:
            print('Job deleted')
            pass

    batch = client_service.new_batch_http_request()
    for job_to_be_deleted in jobs_to_be_deleted:
        batch.add(
            client_service.projects().jobs().delete(
                name=job_to_be_deleted.get('name')),
            callback=job_delete_callback)

    batch.execute()
# [END job_discovery_batch_job_delete]


def run_sample():
    import base_company_sample

    # Create a company before creating jobs
    company_to_be_created = base_company_sample.generate_company()
    company_created = base_company_sample.create_company(
        client_service, company_to_be_created)
    company_name = company_created.get('name')

    created_jobs = batch_job_create(client_service, company_name)
    updated_jobs = batch_job_update(client_service, created_jobs)
    batch_job_delete(client_service, updated_jobs)

    base_company_sample.delete_company(client_service, company_name)


if __name__ == '__main__':
    run_sample()
