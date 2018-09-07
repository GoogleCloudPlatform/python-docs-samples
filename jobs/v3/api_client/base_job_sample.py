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

from googleapiclient.discovery import build
from googleapiclient.errors import Error

client_service = build('jobs', 'v3')
parent = 'projects/' + os.environ['GOOGLE_CLOUD_PROJECT']
# [END instantiate]


# [START basic_job]
def generate_job_with_required_fields(company_name):
    # Requisition id should be a unique Id in your system.
    requisition_id = 'job_with_required_fields:' + ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(16))

    job_title = 'Software Engineer'
    application_uris = ['http://careers.google.com']
    description = ('Design, develop, test, deploy, maintain and improve '
                   'software.')

    job = {
        'requisition_id': requisition_id,
        'title': job_title,
        'application_info': {'uris': application_uris},
        'description': description,
        'company_name': company_name
    }
    print('Job generated: %s' % job)
    return job
# [END basic_job]


# [START create_job]
def create_job(client_service, job_to_be_created):
    try:
        request = {'job': job_to_be_created}
        job_created = client_service.projects().jobs().create(
            parent=parent, body=request).execute()
        print('Job created: %s' % job_created)
        return job_created
    except Error as e:
        print('Got exception while creating job')
        raise e
# [END create_job]


# [START get_job]
def get_job(client_service, job_name):
    try:
        job_existed = client_service.projects().jobs().get(
            name=job_name).execute()
        print('Job existed: %s' % job_existed)
        return job_existed
    except Error as e:
        print('Got exception while getting job')
        raise e
# [END get_job]


# [START update_job]
def update_job(client_service, job_name, job_to_be_updated):
    try:
        request = {'job': job_to_be_updated}
        job_updated = client_service.projects().jobs().patch(
            name=job_name, body=request).execute()
        print('Job updated: %s' % job_updated)
        return job_updated
    except Error as e:
        print('Got exception while updating job')
        raise e
# [END update_job]


# [START update_job_with_field_mask]
def update_job_with_field_mask(client_service, job_name, job_to_be_updated,
                               field_mask):
    try:
        request = {'job': job_to_be_updated, 'update_mask': field_mask}
        job_updated = client_service.projects().jobs().patch(
            name=job_name, body=request).execute()
        print('Job updated: %s' % job_updated)
        return job_updated
    except Error as e:
        print('Got exception while updating job with field mask')
        raise e
# [END update_job_with_field_mask]


# [START delete_job]
def delete_job(client_service, job_name):
    try:
        client_service.projects().jobs().delete(name=job_name).execute()
        print('Job deleted')
    except Error as e:
        print('Got exception while deleting job')
        raise e
# [END delete_job]


def run_sample():
    import base_company_sample

    # Create a company before creating jobs
    company_to_be_created = base_company_sample.generate_company()
    company_created = base_company_sample.create_company(
        client_service, company_to_be_created)
    company_name = company_created.get('name')

    # Construct a job
    job_to_be_created = generate_job_with_required_fields(company_name)

    # Create a job
    job_created = create_job(client_service, job_to_be_created)

    # Get a job
    job_name = job_created.get('name')
    get_job(client_service, job_name)

    # Update a job
    job_to_be_updated = job_created
    job_to_be_updated.update({'description': 'changedDescription'})
    update_job(client_service, job_name, job_to_be_updated)

    # Update a job with field mask
    update_job_with_field_mask(client_service, job_name,
                               {'title': 'changedJobTitle'}, 'title')

    # Delete a job
    delete_job(client_service, job_name)

    # Delete company only after cleaning all jobs under this company
    base_company_sample.delete_company(client_service, company_name)


if __name__ == '__main__':
    run_sample()
