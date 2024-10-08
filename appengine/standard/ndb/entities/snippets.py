# Copyright 2016 Google Inc.
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


def create_entity_using_keyword_arguments():
    sandy = Account(username="Sandy", userid=123, email="sandy@example.com")
    return sandy


def create_entity_using_attributes():
    sandy = Account()
    sandy.username = "Sandy"
    sandy.userid = 123
    sandy.email = "sandy@example.com"
    return sandy


def create_entity_using_populate():
    sandy = Account()
    sandy.populate(username="Sandy", userid=123, email="sandy@gmail.com")
    return sandy


def demonstrate_model_constructor_type_checking():
    bad = Account(username="Sandy", userid="not integer")  # raises an exception
    return bad


def demonstrate_entity_attribute_type_checking(sandy):
    sandy.username = 42  # raises an exception


def save_entity(sandy):
    sandy_key = sandy.put()
    return sandy_key


def get_entity(sandy_key):
    sandy = sandy_key.get()
    return sandy


def get_key_kind_and_id(sandy_key):
    kind_string = sandy_key.kind()  # returns 'Account'
    ident = sandy_key.id()  # returns '2'
    return kind_string, ident


def get_url_safe_key(sandy_key):
    url_string = sandy_key.urlsafe()
    return url_string


def get_entity_from_url_safe_key(url_string):
    sandy_key = ndb.Key(urlsafe=url_string)
    sandy = sandy_key.get()
    return sandy


def get_key_and_numeric_id_from_url_safe_key(url_string):
    key = ndb.Key(urlsafe=url_string)
    kind_string = key.kind()
    ident = key.id()
    return key, ident, kind_string


def update_entity_from_key(key):
    sandy = key.get()
    sandy.email = "sandy@example.co.uk"
    sandy.put()


def delete_entity(sandy):
    sandy.key.delete()


def create_entity_with_named_key():
    account = Account(
        username="Sandy", userid=1234, email="sandy@example.com", id="sandy@example.com"
    )

    return account.key.id()  # returns 'sandy@example.com'


def set_key_directly(account):
    account.key = ndb.Key("Account", "sandy@example.com")

    # You can also use the model class object itself, rather than its name,
    # to specify the entity's kind:
    account.key = ndb.Key(Account, "sandy@example.com")


def create_entity_with_generated_id():
    # note: no id kwarg
    account = Account(username="Sandy", userid=1234, email="sandy@example.com")
    account.put()
    # account.key will now have a key of the form: ndb.Key(Account, 71321839)
    # where the value 71321839 was generated by Datastore for us.
    return account


class Revision(ndb.Model):
    message_text = ndb.StringProperty()


def demonstrate_entities_with_parent_hierarchy():
    ndb.Key("Account", "sandy@example.com", "Message", 123, "Revision", "1")
    ndb.Key("Account", "sandy@example.com", "Message", 123, "Revision", "2")
    ndb.Key("Account", "larry@example.com", "Message", 456, "Revision", "1")
    ndb.Key("Account", "larry@example.com", "Message", 789, "Revision", "2")


def equivalent_ways_to_define_key_with_parent():
    ndb.Key("Account", "sandy@example.com", "Message", 123, "Revision", "1")

    ndb.Key(
        "Revision", "1", parent=ndb.Key("Account", "sandy@example.com", "Message", 123)
    )

    ndb.Key(
        "Revision",
        "1",
        parent=ndb.Key("Message", 123, parent=ndb.Key("Account", "sandy@example.com")),
    )


def create_root_key():
    sandy_key = ndb.Key(Account, "sandy@example.com")
    return sandy_key


def create_entity_with_parent_keys():
    account_key = ndb.Key(Account, "sandy@example.com")

    # Ask Datastore to allocate an ID.
    new_id = ndb.Model.allocate_ids(size=1, parent=account_key)[0]

    # Datastore returns us an integer ID that we can use to create the message
    # key
    message_key = ndb.Key("Message", new_id, parent=account_key)

    # Now we can put the message into Datastore
    initial_revision = Revision(message_text="Hello", id="1", parent=message_key)
    initial_revision.put()

    return initial_revision


def get_parent_key_of_entity(initial_revision):
    message_key = initial_revision.key.parent()
    return message_key


def operate_on_multiple_keys_at_once(list_of_entities):
    list_of_keys = ndb.put_multi(list_of_entities)
    list_of_entities = ndb.get_multi(list_of_keys)
    ndb.delete_multi(list_of_keys)


class Mine(ndb.Expando):
    pass


def create_entity_using_expando_model():
    e = Mine()
    e.foo = 1
    e.bar = "blah"
    e.tags = ["exp", "and", "oh"]
    e.put()

    return e


def get_properties_defined_on_expando(e):
    return e._properties
    # {
    #     'foo': GenericProperty('foo'),
    #     'bar': GenericProperty('bar'),
    #     'tags': GenericProperty('tags', repeated=True)
    # }


class FlexEmployee(ndb.Expando):
    name = ndb.StringProperty()
    age = ndb.IntegerProperty()


def create_expando_model_entity_with_defined_properties():
    employee = FlexEmployee(name="Sandy", location="SF")
    return employee


class Specialized(ndb.Expando):
    _default_indexed = False


def create_expando_model_entity_that_isnt_indexed_by_default():
    e = Specialized(foo="a", bar=["b"])
    return e._properties
    # {
    #     'foo': GenericProperty('foo', indexed=False),
    #     'bar': GenericProperty('bar', indexed=False, repeated=True)
    # }


def demonstrate_wrong_way_to_query_expando():
    FlexEmployee.query(FlexEmployee.location == "SF")


def demonstrate_right_way_to_query_expando():
    FlexEmployee.query(ndb.GenericProperty("location") == "SF")


notification = None


def _notify(message):
    global notification
    notification = message


class Friend(ndb.Model):
    name = ndb.StringProperty()

    def _pre_put_hook(self):
        _notify("Gee wiz I have a new friend!")

    @classmethod
    def _post_delete_hook(cls, key, future):
        _notify("I have found occasion to rethink our friendship.")


def demonstrate_model_put_and_delete_hooks():
    f = Friend()
    f.name = "Carole King"
    f.put()  # _pre_put_hook is called
    yield f
    fut = f.key.delete_async()  # _post_delete_hook not yet called
    fut.get_result()  # _post_delete_hook is called
    yield f


class MyModel(ndb.Model):
    pass


def reserve_model_ids():
    first, last = MyModel.allocate_ids(100)
    return first, last


def reserve_model_ids_with_a_parent(p):
    first, last = MyModel.allocate_ids(100, parent=p)
    return first, last


def construct_keys_from_range_of_reserved_ids(first, last):
    keys = [ndb.Key(MyModel, id) for id in range(first, last + 1)]
    return keys


def reserve_model_ids_up_to(N):
    first, last = MyModel.allocate_ids(max=N)
    return first, last


class ModelWithUser(ndb.Model):
    user_id = ndb.StringProperty()
    color = ndb.StringProperty()

    @classmethod
    def get_by_user(cls, user):
        return cls.query().filter(cls.user_id == user.user_id()).get()
