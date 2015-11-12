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

"""A simple model for representing an address book contact.

For more information, see README.md.
"""

# This is the first naive model for starting the article.  In the
# older version of this article with db module, we used
# PhoneNumberProperty and PostalAddressProperty. With ndb, there are
# no properties like those, so we just use StringProperty instead.


from google.appengine.ext import ndb


# [START naive_models]
class Contact(ndb.Model):
    """A naive Contact model."""
    # Basic info.
    name = ndb.StringProperty()
    birth_day = ndb.DateProperty()

    # Address info.
    address = ndb.StringProperty()

    # Phone info.
    phone_number = ndb.StringProperty()

    # Company info.
    company_title = ndb.StringProperty()
    company_name = ndb.StringProperty()
    company_description = ndb.TextProperty()
    company_address = ndb.StringProperty()
# [END naive_models]
