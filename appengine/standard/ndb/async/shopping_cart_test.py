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
import pytest

import shopping_cart


@pytest.fixture
def items(testbed):
    account = shopping_cart.Account(id='123')
    account.put()

    items = [shopping_cart.InventoryItem(name='Item {}'.format(i))
             for i in range(6)]
    special_items = [shopping_cart.InventoryItem(name='Special {}'.format(i))
                     for i in range(6)]
    for i in items + special_items:
        i.put()

    special_offers = [shopping_cart.SpecialOffer(inventory=item.key)
                      for item in special_items]
    cart_items = [
        shopping_cart.CartItem(
            account=account.key, inventory=item.key, quantity=i)
        for i, item in enumerate(items[:6] + special_items[:6])]
    for i in special_offers + cart_items:
        i.put()

    return account, items, special_items, cart_items, special_offers


def test_get_cart_plus_offers(items):
    account, items, special_items, cart_items, special_offers = items

    cart, offers = shopping_cart.get_cart_plus_offers(account)

    assert len(cart) == 12
    assert len(offers) == 6


def test_get_cart_plus_offers_async(items):
    account, items, special_items, cart_items, special_offers = items

    cart, offers = shopping_cart.get_cart_plus_offers_async(account)

    assert len(cart) == 12
    assert len(offers) == 6


def test_get_cart_tasklet(items):
    account, items, special_items, cart_items, special_offers = items

    future = shopping_cart.get_cart_tasklet(account)
    cart = future.get_result()

    assert len(cart) == 12


def test_get_offers_tasklet(items):
    account, items, special_items, cart_items, special_offers = items

    future = shopping_cart.get_offers_tasklet(account)
    offers = future.get_result()

    assert len(offers) == 6


def test_get_cart_plus_offers_tasklet(items):
    account, items, special_items, cart_items, special_offers = items

    future = shopping_cart.get_cart_plus_offers_tasklet(
        account)
    cart, offers = future.get_result()

    assert len(cart) == 12
    assert len(offers) == 6


def test_iterate_over_query_results_in_tasklet(items):
    account, items, special_items, cart_items, special_offers = items

    future = shopping_cart.iterate_over_query_results_in_tasklet(
        shopping_cart.InventoryItem, lambda item: '3' in item.name)

    assert '3' in future.get_result().name


def test_do_not_iterate_over_tasklet_like_this(items):
    account, items, special_items, cart_items, special_offers = items

    future = shopping_cart.blocking_iteration_over_query_results(
        shopping_cart.InventoryItem, lambda item: '3' in item.name)

    assert '3' in future.get_result().name


def test_get_google(testbed):
    testbed.init_urlfetch_stub()

    get_google = shopping_cart.define_get_google()
    future = get_google()
    assert 'Google' in future.get_result()


class Counter(ndb.Model):
    value = ndb.IntegerProperty()


def test_update_counter_async(testbed):
    counter_key = Counter(value=1).put()
    update_counter = shopping_cart.define_update_counter_async()
    future = update_counter(counter_key)
    assert counter_key.get().value == 1
    assert future.get_result() == 2
    assert counter_key.get().value == 2


def test_update_counter_tasklet(testbed):
    counter_key = Counter(value=1).put()
    update_counter = shopping_cart.define_update_counter_tasklet()
    future = update_counter(counter_key)
    assert counter_key.get().value == 1
    future.get_result()
    assert counter_key.get().value == 2


def test_get_first_ready(testbed):
    testbed.init_urlfetch_stub()

    content = shopping_cart.get_first_ready()
    assert 'html' in content.lower()
