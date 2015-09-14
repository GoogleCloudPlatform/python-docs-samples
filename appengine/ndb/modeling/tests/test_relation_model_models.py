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

from appengine.ndb.modeling import relation_model_models as models
from google.appengine.ext import ndb
from tests import AppEngineTestbedCase


class ContactTestCase(AppEngineTestbedCase):
    """A test case for the Contact model with relationship model."""
    def setUp(self):
        """Creates 1 contact and 1 company.

        Assuming the contact belongs to tmatsuo's addressbook.
        """
        super(ContactTestCase, self).setUp()
        self.myaddressbook_key = ndb.Key('AddressBook', 'tmatsuo')
        mary = models.Contact(parent=self.myaddressbook_key, name='Mary')
        mary.put()
        self.mary_key = mary.key
        google = models.Company(name='Google')
        google.put()
        self.google_key = google.key
        candit = models.Company(name='Candit')
        candit.put()
        self.candit_key = candit.key

    def test_relationship(self):
        """Two companies hire Mary."""
        mary = self.mary_key.get()
        google = self.google_key.get()
        candit = self.candit_key.get()
        # first google hires Mary
        models.ContactCompany(parent=self.myaddressbook_key,
                              contact=mary.key,
                              company=google.key,
                              title='engineer').put()
        # then another company named 'candit' hires Mary too
        models.ContactCompany(parent=self.myaddressbook_key,
                              contact=mary.key,
                              company=candit.key,
                              title='president').put()
        # get the list of companies that Mary belongs to
        self.assertEqual(len(mary.companies), 2)
