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

"""Models for representing an address book contact with grouping.

This module provides models which implement structured properties,
strongly consistent querying, and one-to-many grouping.

For more information, see README.md.
"""


from google.appengine.ext import ndb


# [START contact_with_group_models]
class PhoneNumber(ndb.Model):
    """A model representing a phone number."""
    phone_type = ndb.StringProperty(
        choices=('home', 'work', 'fax', 'mobile', 'other'))
    number = ndb.StringProperty()


class Group(ndb.Model):
    """A model representing groups.

    Expects to have a parent key with the id of the addressbook owner.

    Example: assume my username is tmatsuo

        addrbook_key = ndb.Key('AddressBook', 'tmatsuo')
        friends = models.Group(parent=addrbook_key, name="friends")
        friends.put()
    """
    name = ndb.StringProperty()
    description = ndb.TextProperty()

    @property
    def members(self):
        """Returns a query object with myself as an ancestor."""
        return Contact.query(ancestor=self.key.parent()).filter(
            Contact.groups == self.key)


class Contact(ndb.Model):
    """A Contact model that uses repeated KeyProperty.

    Expects to have a parent key with the id of the addressbook owner.

    Example: assume my username is tmatsuo

        addrbook_key = ndb.Key('AddressBook', 'tmatsuo')
        mary = models.Contact(parent=addrbook_key, name='mary', ...)
        mary.put()
    """
    # Basic info.
    name = ndb.StringProperty()
    birth_day = ndb.DateProperty()

    # Address info.
    address = ndb.StringProperty()

    phone_numbers = ndb.StructuredProperty(PhoneNumber, repeated=True)

    # Company info.
    company_title = ndb.StringProperty()
    company_name = ndb.StringProperty()
    company_description = ndb.TextProperty()
    company_address = ndb.StringProperty()

    # Group affiliation
    groups = ndb.KeyProperty(Group, repeated=True)
# [END contact_with_group_models]
