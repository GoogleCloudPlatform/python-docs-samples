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


"""Models for representing a contact with multiple phone numbers.

This module provides models with a relationship with ndb.KeyProperty to
allow a single contact to have multiple phone numbers.

For more information, see README.md.
"""


# In the original article, it uses ReferenceProperty on the
# PhoneNumber model. With ndb, there is no ReferenceProperty any more,
# so here we use KeyProperty first. However this pattern has a
# consistency issue, shown in the test_fails function in
# test/test_keyproperty_models.py.


from google.appengine.ext import ndb


# [START keyproperty_models]
class Contact(ndb.Model):
    """A Contact model with KeyProperty."""
    # Basic info.
    name = ndb.StringProperty()
    birth_day = ndb.DateProperty()

    # Address info.
    address = ndb.StringProperty()

    # Company info.
    company_title = ndb.StringProperty()
    company_name = ndb.StringProperty()
    company_description = ndb.TextProperty()
    company_address = ndb.StringProperty()

    # The original phone_number property has been replaced by
    # the following property.
    @property
    def phone_numbers(self):
        return PhoneNumber.query(PhoneNumber.contact == self.key)


class PhoneNumber(ndb.Model):
    """A model representing a phone number."""
    contact = ndb.KeyProperty(Contact)
    phone_type = ndb.StringProperty(
        choices=('home', 'work', 'fax', 'mobile', 'other'))
    number = ndb.StringProperty()
# [END keyproperty_models]
