# Copyright 2014 Google Inc. All Rights Reserved.
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

"""Test classes for code snippet for modeling article."""

from google.appengine.ext import ndb
import pytest

import parent_child_models as models


NAME = 'Takashi Matsuo'


@pytest.fixture
def contact_key(testbed):
    contact = models.Contact(name=NAME)
    contact.put()
    return contact.key


def test_basic(contact_key):
    contact = contact_key.get()
    assert contact.name == NAME


# [START succeeding_test]
def test_success(contact_key):
    contact = contact_key.get()
    models.PhoneNumber(parent=contact_key,
                       phone_type='home',
                       number='(650) 555 - 2200').put()
    numbers = contact.phone_numbers.fetch()
    assert 1 == len(numbers)
# [START succeeding_test]


def test_phone_numbers(contact_key):
    """A test for 'phone_numbers' property."""
    models.PhoneNumber(parent=contact_key,
                       phone_type='home',
                       number='(650) 555 - 2200').put()
    models.PhoneNumber(parent=contact_key,
                       phone_type='mobile',
                       number='(650) 555 - 2201').put()
    contact = contact_key.get()
    for phone in contact.phone_numbers:
        # it doesn't ensure any order
        if phone.phone_type == 'home':
            assert '(650) 555 - 2200' == phone.number
        elif phone.phone_type == 'mobile':
            assert phone.number == '(650) 555 - 2201'

    # filer the phone numbers by type. Note that this is an
    # ancestor query.
    query = contact.phone_numbers.filter(
        models.PhoneNumber.phone_type == 'home')
    entities = query.fetch()
    assert 1 == len(entities)
    assert entities[0].number == '(650) 555 - 2200'

    # delete the mobile phones
    query = contact.phone_numbers.filter(
        models.PhoneNumber.phone_type == 'mobile')
    ndb.delete_multi([e.key for e in query])

    # make sure there's no mobile phones any more
    query = contact.phone_numbers.filter(
        models.PhoneNumber.phone_type == 'mobile')
    entities = query.fetch()
    assert 0 == len(entities)
