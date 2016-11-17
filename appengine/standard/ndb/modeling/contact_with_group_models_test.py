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

from google.appengine.ext import ndb

import contact_with_group_models as models


def test_models(testbed):
    # Creates 3 contacts and 1 group.
    # Assuming the group and contacts are private and belong to tmatsuo's
    # addressbook.
    addressbook_key = ndb.Key('AddressBook', 'tmatsuo')

    friends = models.Group(parent=addressbook_key, name='friends')
    friends.put()
    friends_key = friends.key
    mary = models.Contact(parent=addressbook_key, name='Mary')
    mary.put()
    mary_key = mary.key

    # Add Mary to your 'friends' group
    mary = mary_key.get()
    friends = friends_key.get()
    if friends.key not in mary.groups:
        mary.groups.append(friends.key)
        mary.put()

    # Now Mary is your friend
    mary = mary_key.get()
    assert friends.key in mary.groups

    # How about 'members' property?
    friend_list = friends.members.fetch()
    assert len(friend_list) == 1
