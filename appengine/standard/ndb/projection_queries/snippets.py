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


class Article(ndb.Model):
    title = ndb.StringProperty()
    author = ndb.StringProperty()
    tags = ndb.StringProperty(repeated=True)


def print_author_tags():
    query = Article.query()
    articles = query.fetch(20, projection=[Article.author, Article.tags])
    for article in articles:
        print(article.author)
        print(article.tags)
        # article.title will raise a ndb.UnprojectedPropertyError


class Address(ndb.Model):
    type = ndb.StringProperty()  # E.g., 'home', 'work'
    street = ndb.StringProperty()
    city = ndb.StringProperty()


class Contact(ndb.Model):
    name = ndb.StringProperty()
    addresses = ndb.StructuredProperty(Address, repeated=True)


def fetch_sub_properties():
    Contact.query().fetch(projection=["name", "addresses.city"])
    Contact.query().fetch(projection=[Contact.name, Contact.addresses.city])


def demonstrate_ndb_grouping():
    Article.query(projection=[Article.author], group_by=[Article.author])
    Article.query(projection=[Article.author], distinct=True)


class Foo(ndb.Model):
    A = ndb.IntegerProperty(repeated=True)
    B = ndb.StringProperty(repeated=True)


def declare_multiple_valued_property():
    entity = Foo(A=[1, 1, 2, 3], B=['x', 'y', 'x'])
    return entity
