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


import unittest

from datastore.ndb.modeling import naive_models as models

import test_base


class ContactTestCase(test_base.TestCase):
    """A test case for the naive Contact model classe."""
    NAME = 'Takashi Matsuo'

    def setUp(self):
        super(ContactTestCase, self).setUp()
        contact = models.Contact(name=self.NAME)
        contact.put()
        self.contact_key = contact.key

    def test_basic(self):
        """Test for getting a NaiveContact entity."""
        contact = self.contact_key.get()
        self.assertEqual(contact.name, self.NAME)


if __name__ == '__main__':
    unittest.main()
