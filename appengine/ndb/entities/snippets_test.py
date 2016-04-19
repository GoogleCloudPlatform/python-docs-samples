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

import inspect

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.ndb.google_imports import datastore_errors
import pytest
import snippets


@pytest.yield_fixture
def client(testbed):
    yield testbed

    for name, obj in inspect.getmembers(snippets):
        if inspect.isclass(obj) and issubclass(obj, ndb.Model):
            ndb.delete_multi(obj.query().iter(keys_only=True))


def test_create_model_using_keyword_arguments(client):
    result = snippets.create_model_using_keyword_arguments()
    assert isinstance(result, snippets.Account)


def test_create_model_using_attributes(client):
    result = snippets.create_model_using_attributes()
    assert isinstance(result, snippets.Account)


def test_create_model_using_populate(client):
    result = snippets.create_model_using_populate()
    assert isinstance(result, snippets.Account)


def test_demonstrate_model_constructor_type_checking(client):
    with pytest.raises(datastore_errors.BadValueError):
        snippets.demonstrate_model_constructor_type_checking()


def test_dmonstrate_model_attribute_type_checking(client):
    with pytest.raises(datastore_errors.BadValueError):
        snippets.dmonstrate_model_attribute_type_checking(
            snippets.create_model_using_keyword_arguments())


def test_save_model(client):
    result = snippets.save_model(
        snippets.create_model_using_keyword_arguments())
    assert isinstance(result, snippets.ndb.Key)


def test_get_model(client):
    sandy_key = snippets.save_model(
        snippets.create_model_using_keyword_arguments())
    result = snippets.get_model(sandy_key)
    assert isinstance(result, snippets.Account)


def test_get_key_kind_and_id(client):
    sandy_key = snippets.save_model(
        snippets.create_model_using_keyword_arguments())
    kind_string, ident = snippets.get_key_kind_and_id(sandy_key)
    assert kind_string == 'Account'
    assert isinstance(ident, long)


def test_get_url_safe_key(client):
    sandy_key = snippets.save_model(
        snippets.create_model_using_keyword_arguments())
    result = snippets.get_url_safe_key(sandy_key)
    assert isinstance(result, str)


def test_get_model_from_url_safe_key(client):
    sandy_key = snippets.save_model(
        snippets.create_model_using_keyword_arguments())
    result = snippets.get_model_from_url_safe_key(
        snippets.get_url_safe_key(sandy_key))
    assert isinstance(result, snippets.Account)
    assert result.username == 'Sandy'


def test_get_key_and_numeric_id_from_url_safe_key(client):
    sandy_key = snippets.save_model(
        snippets.create_model_using_keyword_arguments())
    urlsafe = snippets.get_url_safe_key(sandy_key)
    key, ident, kind_string = (
        snippets.get_key_and_numeric_id_from_url_safe_key(urlsafe))
    assert isinstance(key, ndb.Key)
    assert isinstance(ident, long)
    assert isinstance(kind_string, str)


def test_update_model_from_key(client):
    sandy = snippets.create_model_using_keyword_arguments()
    sandy_key = snippets.save_model(sandy)
    urlsafe = snippets.get_url_safe_key(sandy_key)
    key, ident, kind_string = (
        snippets.get_key_and_numeric_id_from_url_safe_key(urlsafe))
    snippets.update_model_from_key(key)
    assert key.get().email == 'sandy@example.co.uk'


def test_delete_model(client):
    sandy = snippets.create_model_using_keyword_arguments()
    snippets.save_model(sandy)
    snippets.delete_model(sandy)
    assert sandy.key.get() is None


def test_create_model_with_named_key(client):
    result = snippets.create_model_with_named_key()
    assert 'sandy@example.com' == result


def test_set_key_directly(client):
    account = snippets.Account()
    snippets.set_key_directly(account)
    assert account.key.id() == 'sandy@example.com'


def test_create_model_with_generated_id(client):
    result = snippets.create_model_with_generated_id()
    assert isinstance(result.key.id(), long)


def test_demonstrate_models_with_parent_hierarchy(client):
    snippets.demonstrate_models_with_parent_hierarchy()


def test_equivalent_ways_to_define_key_with_parent(client):
    snippets.equivalent_ways_to_define_key_with_parent()


def test_create_root_key(client):
    result = snippets.create_root_key()
    assert result.id() == 'sandy@example.com'


def test_create_model_with_parent_keys(client):
    result = snippets.create_model_with_parent_keys()
    assert result.message_text == 'Hello'


def test_get_parent_key_of_model(client):
    initial_revision = snippets.create_model_with_parent_keys()
    result = snippets.get_parent_key_of_model(initial_revision)
    assert result.kind() == 'Message'


def test_operate_on_multiple_keys_at_once(client):
    snippets.operate_on_multiple_keys_at_once([
        snippets.Account(email='a@a.com'), snippets.Account(email='b@b.com')])


def test_create_expando_model(client):
    result = snippets.create_expando_model()
    assert result.foo == 1


def test_get_properties_defined_on_expando(client):
    result = snippets.get_properties_defined_on_expando(
        snippets.create_expando_model())
    assert result['foo'] is not None
    assert result['bar'] is not None
    assert result['tags'] is not None


def test_create_expando_model_with_defined_properties(client):
    result = snippets.create_expando_model_with_defined_properties()
    assert result.name == 'Sandy'


def test_create_expando_model_that_isnt_indexed_by_default(client):
    result = snippets.create_expando_model_that_isnt_indexed_by_default()
    assert result['foo']
    assert result['bar']


def test_demonstrate_wrong_way_to_query_expando(client):
    with pytest.raises(AttributeError):
        snippets.demonstrate_wrong_way_to_query_expando()


def test_demonstrate_right_way_to_query_expando(client):
    snippets.demonstrate_right_way_to_query_expando()


def test_demonstrate_model_put_and_delete_hooks(client):
    iterator = snippets.demonstrate_model_put_and_delete_hooks()
    iterator.next()
    assert snippets.notification == 'Gee wiz I have a new friend!'
    iterator.next()
    assert snippets.notification == (
        'I have found occasion to rethink our friendship.')


def test_reserve_model_ids(client):
    first, last = snippets.reserve_model_ids()
    assert last - first >= 99


def test_reserve_model_ids_with_a_parent(client):
    first, last = snippets.reserve_model_ids_with_a_parent(
        snippets.Friend().key)
    assert last - first >= 99


def test_construct_keys_from_range_of_reserved_ids(client):
    result = snippets.construct_keys_from_range_of_reserved_ids(
        *snippets.reserve_model_ids())
    assert len(result) == 100


def test_reserve_model_ids_up_to(client):
    first, last = snippets.reserve_model_ids_up_to(5)
    assert last - first >= 4


def test_model_with_user(client):
    user = users.User(email='user@example.com', _user_id='123')
    item = snippets.ModelWithUser(user_id=user.user_id())
    item.put()
    assert snippets.ModelWithUser.get_by_user(user) == item
