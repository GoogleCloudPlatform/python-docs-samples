# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.appengine.ext import ndb


# [START models]
class Account(ndb.Model):
    pass


class InventoryItem(ndb.Model):
    name = ndb.StringProperty()


class CartItem(ndb.Model):
    account = ndb.KeyProperty(kind=Account)
    inventory = ndb.KeyProperty(kind=InventoryItem)
    quantity = ndb.IntegerProperty()


class SpecialOffer(ndb.Model):
    inventory = ndb.KeyProperty(kind=InventoryItem)
# [END models]


def get_cart_plus_offers(acct):
    cart = CartItem.query(CartItem.account == acct.key).fetch()
    offers = SpecialOffer.query().fetch(10)
    ndb.get_multi([item.inventory for item in cart] +
                  [offer.inventory for offer in offers])
    return cart, offers


def get_cart_plus_offers_async(acct):
    cart_future = CartItem.query(CartItem.account == acct.key).fetch_async()
    offers_future = SpecialOffer.query().fetch_async(10)
    cart = cart_future.get_result()
    offers = offers_future.get_result()
    ndb.get_multi([item.inventory for item in cart] +
                  [offer.inventory for offer in offers])
    return cart, offers


# [START cart_offers_tasklets]
@ndb.tasklet
def get_cart_tasklet(acct):
    cart = yield CartItem.query(CartItem.account == acct.key).fetch_async()
    yield ndb.get_multi_async([item.inventory for item in cart])
    raise ndb.Return(cart)


@ndb.tasklet
def get_offers_tasklet(acct):
    offers = yield SpecialOffer.query().fetch_async(10)
    yield ndb.get_multi_async([offer.inventory for offer in offers])
    raise ndb.Return(offers)


@ndb.tasklet
def get_cart_plus_offers_tasklet(acct):
    cart, offers = yield get_cart_tasklet(acct), get_offers_tasklet(acct)
    raise ndb.Return((cart, offers))
# [END cart_offers_tasklets]


@ndb.tasklet
def iterate_over_query_results_in_tasklet(Model, is_the_entity_i_want):
    qry = Model.query()
    qit = qry.iter()
    while (yield qit.has_next_async()):
        entity = qit.next()
        # Do something with entity
        if is_the_entity_i_want(entity):
            raise ndb.Return(entity)


@ndb.tasklet
def blocking_iteration_over_query_results(Model, is_the_entity_i_want):
    # DO NOT DO THIS IN A TASKLET
    qry = Model.query()
    for entity in qry:
        # Do something with entity
        if is_the_entity_i_want(entity):
            raise ndb.Return(entity)


def define_get_google():
    @ndb.tasklet
    def get_google():
        context = ndb.get_context()
        result = yield context.urlfetch("http://www.google.com/")
        if result.status_code == 200:
            raise ndb.Return(result.content)
        # else return None

    return get_google


def define_update_counter_async():
    @ndb.transactional_async
    def update_counter(counter_key):
        counter = counter_key.get()
        counter.value += 1
        counter.put()
        return counter.value

    return update_counter


def define_update_counter_tasklet():
    @ndb.transactional_tasklet
    def update_counter(counter_key):
        counter = yield counter_key.get_async()
        counter.value += 1
        yield counter.put_async()

    return update_counter


def get_first_ready():
    urls = ["http://www.google.com/", "http://www.blogspot.com/"]
    context = ndb.get_context()
    futures = [context.urlfetch(url) for url in urls]
    first_future = ndb.Future.wait_any(futures)
    return first_future.get_result().content
