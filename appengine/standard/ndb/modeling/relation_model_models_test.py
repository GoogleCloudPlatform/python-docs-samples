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

import relation_model_models as models


def test_relationship(testbed):
    # Creates 1 contact and 2 companies
    addressbook_key = ndb.Key('AddressBook', 'tmatsuo')
    mary = models.Contact(parent=addressbook_key, name='Mary')
    mary.put()
    google = models.Company(name='Google')
    google.put()
    candit = models.Company(name='Candit')
    candit.put()

    # first google hires Mary
    models.ContactCompany(parent=addressbook_key,
                          contact=mary.key,
                          company=google.key,
                          title='engineer').put()
    # then another company named 'candit' hires Mary too
    models.ContactCompany(parent=addressbook_key,
                          contact=mary.key,
                          company=candit.key,
                          title='president').put()

    # get the list of companies that Mary belongs to
    assert len(mary.companies) == 2
