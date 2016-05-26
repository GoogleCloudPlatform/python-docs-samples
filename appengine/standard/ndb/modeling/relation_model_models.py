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

"""Models for representing a contact with multiple titles and groups.

This module provides models with structured properties, strong
consistent querying, one-to-many grouping, many-to-many relationships.

For more information, see README.md.
"""


from google.appengine.ext import ndb


# [START relation_model_models]
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
    """A model representing a contact entry.

    Expects to have a parent key with the id of the addressbook owner.

    Example: assume my username is tmatsuo

        addrbook_key = ndb.Key('AddressBook', 'tmatsuo')
        mary = models.Contact(parent=addrbook_key, name='Mary', ...)
        mary.put()
    """
    # Basic info.
    name = ndb.StringProperty()
    birth_day = ndb.DateProperty()

    # Address info.
    address = ndb.StringProperty()

    phone_numbers = ndb.StructuredProperty(PhoneNumber, repeated=True)

    # Group affiliation
    groups = ndb.KeyProperty(Group, repeated=True)

    # The original organization properties have been replaced by
    # the following property.
    @property
    def companies(self):
        rels = ContactCompany.query(ancestor=self.key.parent()).filter(
            ContactCompany.contact == self.key)
        keys = [rel.company for rel in rels]
        return ndb.get_multi(keys)


class Company(ndb.Model):
    """A model representing a company."""
    name = ndb.StringProperty()
    description = ndb.TextProperty()
    company_address = ndb.StringProperty()


class ContactCompany(ndb.Model):
    """A model representing a relation between a contact and a company.

    Expects to have a parent key with the id of the addressbook owner.

    Example: assume my username is tmatsuo

        addrbook_key = ndb.Key('AddressBook', 'tmatsuo')
        mary = models.Contact(parent=addrbook_key, name='Mary', ...)
        mary.put()
        models.ContactCompany(parent=addrbook_key, contact=mary.key,
                              company=google.key, title='engineer').put()
    """
    contact = ndb.KeyProperty(Contact, required=True)
    company = ndb.KeyProperty(Company, required=True)
    title = ndb.StringProperty()
# [END relation_model_models]
