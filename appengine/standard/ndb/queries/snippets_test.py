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

from guestbook import Greeting

import snippets
from snippets_models import (Account, Address, Article,
                             Bar, Contact, FlexEmployee, Message)


def test_query_account_equality(testbed):
    Account(userid=42).put()
    Account(userid=43).put()

    query = snippets.query_account_equality()
    accounts = query.fetch()

    assert len(accounts) == 1
    assert accounts[0].userid == 42


def test_query_account_inequality(testbed):
    Account(userid=32).put()
    Account(userid=42).put()
    Account(userid=43).put()

    query = snippets.query_account_inequality()
    accounts = query.fetch()

    assert len(accounts) == 2
    assert all(a.userid > 40 for a in accounts)


def test_query_account_multiple_filters(testbed):
    Account(userid=40).put()
    Account(userid=49).put()
    Account(userid=50).put()
    Account(userid=6).put()
    Account(userid=62).put()

    query = snippets.query_account_multiple_filters()
    accounts = query.fetch()

    assert len(accounts) == 2
    assert all(40 <= a.userid < 50 for a in accounts)


def test_query_account_in_steps(testbed):
    Account(userid=40).put()
    Account(userid=49).put()
    Account(userid=50).put()
    Account(userid=6).put()
    Account(userid=62).put()

    _, _, query = snippets.query_account_in_steps()
    accounts = query.fetch()

    assert len(accounts) == 2
    assert all(40 <= a.userid < 50 for a in accounts)


def test_query_article_inequality(testbed):
    Article(tags=['perl']).put()
    Article(tags=['perl', 'python']).put()

    query = snippets.query_article_inequality()
    articles = query.fetch()

    assert len(articles) == 1


def test_query_article_inequality_explicit(testbed):
    Article(tags=['perl']).put()
    Article(tags=['perl', 'python']).put()

    query = snippets.query_article_inequality_explicit()
    articles = query.fetch()

    assert len(articles) == 1


def test_articles_with_tags_example(testbed):
    snippets.articles_with_tags_example()


def test_query_article_in(testbed):
    Article(tags=['perl']).put()
    Article(tags=['perl', 'python']).put()
    Article(tags=['ruby']).put()
    Article(tags=['php']).put()

    query = snippets.query_article_in()
    articles = query.fetch()

    assert len(articles) == 3


def test_query_article_in_equivalent(testbed):
    Article(tags=['perl']).put()
    Article(tags=['perl', 'python']).put()
    Article(tags=['ruby']).put()
    Article(tags=['php']).put()

    query = snippets.query_article_in_equivalent()
    articles = query.fetch()

    assert len(articles) == 3


def test_query_article_nested(testbed):
    Article(tags=['python']).put()  # excluded - no non-python
    Article(tags=['ruby']).put()  # excluded - no python
    Article(tags=['python', 'ruby']).put()  # included
    Article(tags=['python', 'jruby']).put()  # included
    Article(tags=['python', 'ruby', 'jruby']).put()  # included
    Article(tags=['python', 'php']).put()  # included
    Article(tags=['python', 'perl']).put()  # excluded

    query = snippets.query_article_nested()
    articles = query.fetch()
    assert len(articles) == 4


def test_query_greeting_order(testbed):
    Greeting(content='3').put()
    Greeting(content='2').put()
    Greeting(content='1').put()
    Greeting(content='2').put()

    query = snippets.query_greeting_order()
    greetings = query.fetch()

    assert (greetings[0].content < greetings[1].content < greetings[3].content)
    assert greetings[1].content == greetings[2].content
    assert greetings[1].date > greetings[2].date


def test_query_greeting_multiple_orders(testbed):
    Greeting(content='3').put()
    Greeting(content='2').put()
    Greeting(content='1').put()
    Greeting(content='2').put()

    query = snippets.query_greeting_multiple_orders()
    greetings = query.fetch()

    assert (greetings[0].content < greetings[1].content < greetings[3].content)
    assert greetings[1].content == greetings[2].content
    assert greetings[1].date > greetings[2].date


def test_query_purchase_with_customer_key(testbed):
    Customer, Purchase, do_query = snippets.query_purchase_with_customer_key()
    charles = Customer(name='Charles')
    charles.put()
    snoop_key = Customer(name='Snoop').put()
    Purchase(price=123, customer=charles.key).put()
    Purchase(price=234, customer=snoop_key).put()

    purchases = do_query(charles)
    assert len(purchases) == 1
    assert purchases[0].price == 123


def test_query_purchase_with_ancestor_key(testbed):
    Customer, Purchase, create_purchase, do_query = (
        snippets.query_purchase_with_ancestor_key())
    charles = Customer(name='Charles')
    charles.put()
    snoop = Customer(name='Snoop')
    snoop.put()

    charles_purchase = create_purchase(charles)
    charles_purchase.price = 123
    charles_purchase.put()

    snoop_purchase = create_purchase(snoop)
    snoop_purchase.price = 234
    snoop_purchase.put()

    purchases = do_query(snoop)
    assert len(purchases) == 1
    assert purchases[0].price == 234


def test_print_query(testbed, capsys):
    snippets.print_query()
    stdout, _ = capsys.readouterr()

    assert '' in stdout


def test_query_contact_with_city(testbed):
    address = Address(type='home', street='Spear St', city='Amsterdam')
    address.put()
    Contact(name='Bertus Aafjes', addresses=[address]).put()
    address1 = Address(type='home', street='Damrak St', city='Amsterdam')
    address1.put()
    address2 = Address(type='work', street='Spear St', city='San Francisco')
    address2.put()
    Contact(name='Willem Jan Aalders', addresses=[address1, address2]).put()
    address = Address(type='home', street='29th St', city='San Francisco')
    address.put()
    Contact(name='Hans Aarsman', addresses=[address]).put()

    query = snippets.query_contact_with_city()
    contacts = query.fetch()

    assert len(contacts) == 2


def test_query_contact_sub_entities_beware(testbed):
    address = Address(type='home', street='Spear St', city='Amsterdam')
    address.put()
    Contact(name='Bertus Aafjes', addresses=[address]).put()
    address1 = Address(type='home', street='Damrak St', city='Amsterdam')
    address1.put()
    address2 = Address(type='work', street='Spear St', city='San Francisco')
    address2.put()
    Contact(name='Willem Jan Aalders', addresses=[address1, address2]).put()
    address = Address(type='home', street='29th St', city='San Francisco')
    address.put()
    Contact(name='Hans Aarsman', addresses=[address]).put()

    query = snippets.query_contact_sub_entities_beware()
    contacts = query.fetch()

    assert len(contacts) == 2
    for contact in contacts:
        assert ('Spear St' in [a.street for a in contact.addresses] or
                'Amsterdam' in [a.city for a in contact.addresses])


def test_query_contact_multiple_values_in_single_sub_entity(testbed):
    address = Address(type='home', street='Spear St', city='Amsterdam')
    address.put()
    Contact(name='Bertus Aafjes', addresses=[address]).put()
    address1 = Address(type='home', street='Damrak St', city='Amsterdam')
    address1.put()
    address2 = Address(type='work', street='Spear St', city='San Francisco')
    address2.put()
    Contact(name='Willem Jan Aalders', addresses=[address1, address2]).put()
    address = Address(type='home', street='29th St', city='San Francisco')
    address.put()
    Contact(name='Hans Aarsman', addresses=[address]).put()

    query = snippets.query_contact_multiple_values_in_single_sub_entity()
    contacts = query.fetch()

    assert len(contacts) == 1
    assert any(a.city == 'San Francisco' and a.street == 'Spear St'
               for a in contacts[0].addresses)


def test_query_properties_named_by_string_on_expando(testbed):
    FlexEmployee(location='SF').put()
    FlexEmployee(location='Amsterdam').put()

    query = snippets.query_properties_named_by_string_on_expando()
    employees = query.fetch()
    assert len(employees) == 1


def test_query_properties_named_by_string_for_defined_properties(testbed):
    Article(title='from').put()
    Article(title='to').put()

    query = snippets.query_properties_named_by_string_for_defined_properties(
        'title', 'from')
    articles = query.fetch()

    assert len(articles) == 1


def test_query_properties_named_by_string_using_getattr(testbed):
    Article(title='from').put()
    Article(title='to').put()

    query = snippets.query_properties_named_by_string_using_getattr(
        'title', 'from')
    articles = query.fetch()

    assert len(articles) == 1


def test_order_query_results_by_property(testbed):
    Article(title='2').put()
    Article(title='1').put()
    FlexEmployee(location=2).put()
    FlexEmployee(location=1).put()
    expando_query, property_query = snippets.order_query_results_by_property(
        'title')

    assert expando_query.fetch()[0].location == 1
    assert property_query.fetch()[0].title == '1'


def test_print_query_keys(testbed, capsys):
    for i in range(3):
        Article(title='title {}'.format(i)).put()

    snippets.print_query_keys(Article.query())

    stdout, _ = capsys.readouterr()
    assert "Key('Article'" in stdout


def test_reverse_queries(testbed):
    for i in range(11):
        Bar().put()

    (bars, cursor, more), (r_bars, r_cursor, r_more) = (
        snippets.reverse_queries())

    assert len(bars) == 10
    assert len(r_bars) == 10

    for prev_bar, bar in zip(bars, bars[1:]):
        assert prev_bar.key < bar.key

    for prev_bar, bar in zip(r_bars, r_bars[1:]):
        assert prev_bar.key > bar.key


def test_fetch_message_accounts_inefficient(testbed):
    for i in range(1, 6):
        Account(username='Account %s' % i, id=i).put()
        Message(content='Message %s' % i, userid=i).put()

    message_account_pairs = snippets.fetch_message_accounts_inefficient(
        Message.query().order(Message.userid))

    assert len(message_account_pairs) == 5

    print repr(message_account_pairs)
    for i in range(1, 6):
        message, account = message_account_pairs[i - 1]
        assert message.content == 'Message %s' % i
        assert account.username == 'Account %s' % i


def test_fetch_message_accounts_efficient(testbed):
    for i in range(1, 6):
        Account(username='Account %s' % i, id=i).put()
        Message(content='Message %s' % i, userid=i).put()

    message_account_pairs = snippets.fetch_message_accounts_efficient(
        Message.query().order(Message.userid))

    assert len(message_account_pairs) == 5

    for i in range(1, 6):
        message, account = message_account_pairs[i - 1]
        assert message.content == 'Message %s' % i
        assert account.username == 'Account %s' % i


def test_fetch_good_articles_using_gql_with_explicit_bind(testbed):
    for i in range(1, 6):
        Article(stars=i).put()

    query, query2 = snippets.fetch_good_articles_using_gql_with_explicit_bind()
    articles = query2.fetch()

    assert len(articles) == 2
    assert all(a.stars > 3 for a in articles)


def test_fetch_good_articles_using_gql_with_inlined_bind(testbed):
    for i in range(1, 6):
        Article(stars=i).put()

    query = snippets.fetch_good_articles_using_gql_with_inlined_bind()
    articles = query.fetch()

    assert len(articles) == 2
    assert all(a.stars > 3 for a in articles)
