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

This module provides models that represent a one-to-many relationship by
embedding a list of related entites using NDB's StructuredProperty.

For more information, see README.md.
"""


from google.appengine.ext import ndb


# [START structured_property_models]
class PhoneNumber(ndb.Model):
    """A model representing a phone number."""
    phone_type = ndb.StringProperty(
        choices=('home', 'work', 'fax', 'mobile', 'other'))
    number = ndb.StringProperty()


class Contact(ndb.Model):
    """A Contact model that uses StructuredProperty for phone numbers."""
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
# [END structured_property_models]
