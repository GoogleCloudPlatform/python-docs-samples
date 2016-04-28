# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.appengine.ext import ndb


class Account(ndb.Model):
    username = ndb.StringProperty()
    userid = ndb.IntegerProperty()
    email = ndb.StringProperty()


class Address(ndb.Model):
    type = ndb.StringProperty()  # E.g., 'home', 'work'
    street = ndb.StringProperty()
    city = ndb.StringProperty()


class Contact(ndb.Model):
    name = ndb.StringProperty()
    addresses = ndb.StructuredProperty(Address, repeated=True)


class Article(ndb.Model):
    title = ndb.StringProperty()
    stars = ndb.IntegerProperty()
    tags = ndb.StringProperty(repeated=True)


class ArticleWithDifferentDatastoreName(ndb.Model):
    title = ndb.StringProperty('t')


class Employee(ndb.Model):
    full_name = ndb.StringProperty('n')
    retirement_age = ndb.IntegerProperty('r')


class Manager(ndb.Model):
    pass


class FlexEmployee(ndb.Expando):
    name = ndb.StringProperty()
    age = ndb.IntegerProperty()


class Bar(ndb.Model):
    pass


class Message(ndb.Model):
    content = ndb.StringProperty()
    userid = ndb.IntegerProperty()
