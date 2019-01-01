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

from guestbook import Greeting
from snippets_models import (Account, Address, Article,
                             Bar, Contact, Employee, FlexEmployee, Manager)


def query_account_equality():
    query = Account.query(Account.userid == 42)
    return query


def query_account_inequality():
    query = Account.query(Account.userid >= 40)
    return query


def query_account_multiple_filters():
    query = Account.query(Account.userid >= 40, Account.userid < 50)
    return query


def query_account_in_steps():
    query1 = Account.query()  # Retrieve all Account entitites
    query2 = query1.filter(Account.userid >= 40)  # Filter on userid >= 40
    query3 = query2.filter(Account.userid < 50)  # Filter on userid < 50 too
    return query1, query2, query3


def query_article_inequality():
    query = Article.query(Article.tags != 'perl')
    return query


def query_article_inequality_explicit():
    query = Article.query(ndb.OR(Article.tags < 'perl',
                                 Article.tags > 'perl'))
    return query


def articles_with_tags_example():
    # [START included_in_inequality]
    Article(title='Perl + Python = Parrot',
            stars=5,
            tags=['python', 'perl'])
    # [END included_in_inequality]
    # [START excluded_from_inequality]
    Article(title='Introduction to Perl',
            stars=3,
            tags=['perl'])
    # [END excluded_from_inequality]


def query_article_in():
    query = Article.query(Article.tags.IN(['python', 'ruby', 'php']))
    return query


def query_article_in_equivalent():
    query = Article.query(ndb.OR(Article.tags == 'python',
                                 Article.tags == 'ruby',
                                 Article.tags == 'php'))
    return query


def query_article_nested():
    query = Article.query(ndb.AND(Article.tags == 'python',
                                  ndb.OR(Article.tags.IN(['ruby', 'jruby']),
                                         ndb.AND(Article.tags == 'php',
                                                 Article.tags != 'perl'))))
    return query


def query_greeting_order():
    query = Greeting.query().order(Greeting.content, -Greeting.date)
    return query


def query_greeting_multiple_orders():
    query = Greeting.query().order(Greeting.content).order(-Greeting.date)
    return query


def query_purchase_with_customer_key():
    # [START purchase_with_customer_key_models]
    class Customer(ndb.Model):
        name = ndb.StringProperty()

    class Purchase(ndb.Model):
        customer = ndb.KeyProperty(kind=Customer)
        price = ndb.IntegerProperty()
    # [END purchase_with_customer_key_models]

    def query_purchases_for_customer_via_key(customer_entity):
        purchases = Purchase.query(
            Purchase.customer == customer_entity.key).fetch()
        return purchases

    return Customer, Purchase, query_purchases_for_customer_via_key


def query_purchase_with_ancestor_key():
    # [START purchase_with_ancestor_key_models]
    class Customer(ndb.Model):
        name = ndb.StringProperty()

    class Purchase(ndb.Model):
        price = ndb.IntegerProperty()
    # [END purchase_with_ancestor_key_models]

    def create_purchase_for_customer_with_ancestor(customer_entity):
        purchase = Purchase(parent=customer_entity.key)
        return purchase

    def query_for_purchases_of_customer_with_ancestor(customer_entity):
        purchases = Purchase.query(ancestor=customer_entity.key).fetch()
        return purchases

    return (Customer, Purchase,
            create_purchase_for_customer_with_ancestor,
            query_for_purchases_of_customer_with_ancestor)


def print_query():
    print(Employee.query())
    # -> Query(kind='Employee')
    print(Employee.query(ancestor=ndb.Key(Manager, 1)))
    # -> Query(kind='Employee', ancestor=Key('Manager', 1))


def query_contact_with_city():
    query = Contact.query(Contact.addresses.city == 'Amsterdam')
    return query


def query_contact_sub_entities_beware():
    query = Contact.query(Contact.addresses.city == 'Amsterdam',  # Beware!
                          Contact.addresses.street == 'Spear St')
    return query


def query_contact_multiple_values_in_single_sub_entity():
    query = Contact.query(Contact.addresses == Address(city='San Francisco',
                                                       street='Spear St'))
    return query


def query_properties_named_by_string_on_expando():
    property_to_query = 'location'
    query = FlexEmployee.query(ndb.GenericProperty(property_to_query) == 'SF')
    return query


def query_properties_named_by_string_for_defined_properties(keyword, value):
    query = Article.query(Article._properties[keyword] == value)
    return query


def query_properties_named_by_string_using_getattr(keyword, value):
    query = Article.query(getattr(Article, keyword) == value)
    return query


def order_query_results_by_property(keyword):
    expando_query = FlexEmployee.query().order(ndb.GenericProperty('location'))

    property_query = Article.query().order(Article._properties[keyword])

    return expando_query, property_query


def print_query_keys(query):
    for key in query.iter(keys_only=True):
        print(key)


def reverse_queries():
    # Set up.
    q = Bar.query()
    q_forward = q.order(Bar.key)
    q_reverse = q.order(-Bar.key)

    # Fetch a page going forward.
    bars, cursor, more = q_forward.fetch_page(10)

    # Fetch the same page going backward.
    r_bars, r_cursor, r_more = q_reverse.fetch_page(10, start_cursor=cursor)

    return (bars, cursor, more), (r_bars, r_cursor, r_more)


def fetch_message_accounts_inefficient(message_query):
    message_account_pairs = []
    for message in message_query:
        key = ndb.Key('Account', message.userid)
        account = key.get()
        message_account_pairs.append((message, account))

    return message_account_pairs


def fetch_message_accounts_efficient(message_query):
    def callback(message):
        key = ndb.Key('Account', message.userid)
        account = key.get()
        return message, account

    message_account_pairs = message_query.map(callback)
    # Now message_account_pairs is a list of (message, account) tuples.
    return message_account_pairs


def fetch_good_articles_using_gql_with_explicit_bind():
    query = ndb.gql("SELECT * FROM Article WHERE stars > :1")
    query2 = query.bind(3)

    return query, query2


def fetch_good_articles_using_gql_with_inlined_bind():
    query = ndb.gql("SELECT * FROM Article WHERE stars > :1", 3)
    return query
