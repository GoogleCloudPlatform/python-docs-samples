#!/usr/bin/env python

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

import random
import string

# [START jobs_instantiate]
from googleapiclient.discovery import build
from googleapiclient.errors import Error

client_service = build('jobs', 'v2')
# [END jobs_instantiate]


# [START jobs_basic_company]
def generate_company():
    # distributor company id should be a unique Id in your system.
    distributor_company_id = 'company:' + ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(16))

    display_name = 'Google'
    hq_location = '1600 Amphitheatre Parkway Mountain View, CA 94043'

    company = {
        'display_name': display_name,
        'distributor_company_id': distributor_company_id,
        'hq_location': hq_location
    }
    print('Company generated: %s' % company)
    return company
# [END jobs_basic_company]


# [START jobs_create_company]
def create_company(client_service, company_to_be_created):
    try:
        company_created = client_service.companies().create(
            body=company_to_be_created).execute()
        print('Company created: %s' % company_created)
        return company_created
    except Error as e:
        print('Got exception while creating company')
        raise e
# [END jobs_create_company]


# [START jobs_get_company]
def get_company(client_service, company_name):
    try:
        company_existed = client_service.companies().get(
            name=company_name).execute()
        print('Company existed: %s' % company_existed)
        return company_existed
    except Error as e:
        print('Got exception while getting company')
        raise e
# [END jobs_get_company]


# [START jobs_update_company]
def update_company(client_service, company_name, company_to_be_updated):
    try:
        company_updated = client_service.companies().patch(
            name=company_name, body=company_to_be_updated).execute()
        print('Company updated: %s' % company_updated)
        return company_updated
    except Error as e:
        print('Got exception while updating company')
        raise e
# [END jobs_update_company]


# [START jobs_update_company_with_field_mask]
def update_company_with_field_mask(client_service, company_name,
                                   company_to_be_updated, field_mask):
    try:
        company_updated = client_service.companies().patch(
            name=company_name,
            body=company_to_be_updated,
            updateCompanyFields=field_mask).execute()
        print('Company updated: %s' % company_updated)
        return company_updated
    except Error as e:
        print('Got exception while updating company with field mask')
        raise e
# [END jobs_update_company_with_field_mask]


# [START jobs_delete_company]
def delete_company(client_service, company_name):
    try:
        client_service.companies().delete(name=company_name).execute()
        print('Company deleted')
    except Error as e:
        print('Got exception while deleting company')
        raise e
# [END jobs_delete_company]


def run_sample():
    # Construct a company
    company_to_be_created = generate_company()

    # Create a company
    company_created = create_company(client_service, company_to_be_created)

    # Get a company
    company_name = company_created.get('name')
    get_company(client_service, company_name)

    # Update a company
    company_to_be_updated = company_created
    company_to_be_updated.update({'website': 'https://elgoog.im/'})
    update_company(client_service, company_name, company_to_be_updated)

    # Update a company with field mask
    update_company_with_field_mask(
        client_service, company_name, {
            'displayName': 'changedTitle',
            'distributorCompanyId': company_created.get('distributorCompanyId')
        }, 'displayName')

    # Delete a company
    delete_company(client_service, company_name)


if __name__ == '__main__':
    run_sample()
