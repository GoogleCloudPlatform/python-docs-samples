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

# [START notestore_imports]
from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
# [END notestore_imports]
from protorpc import messages


class Account(ndb.Model):
    username = ndb.StringProperty()
    userid = ndb.IntegerProperty()
    email = ndb.StringProperty()


class Employee(ndb.Model):
    full_name = ndb.StringProperty('n')
    retirement_age = ndb.IntegerProperty('r')


class Article(ndb.Model):
    title = ndb.StringProperty()
    stars = ndb.IntegerProperty()
    tags = ndb.StringProperty(repeated=True)


def create_article():
    article = Article(
        title='Python versus Ruby',
        stars=3,
        tags=['python', 'ruby'])
    article.put()
    return article


class Address(ndb.Model):
    type = ndb.StringProperty()  # E.g., 'home', 'work'
    street = ndb.StringProperty()
    city = ndb.StringProperty()


class Contact(ndb.Model):
    name = ndb.StringProperty()
    addresses = ndb.StructuredProperty(Address, repeated=True)


class ContactWithLocalStructuredProperty(ndb.Model):
    name = ndb.StringProperty()
    addresses = ndb.LocalStructuredProperty(Address, repeated=True)


def create_contact():
    guido = Contact(
        name='Guido',
        addresses=[
            Address(
                type='home',
                city='Amsterdam'),
            Address(
                type='work',
                street='Spear St',
                city='SF')])

    guido.put()
    return guido


def create_contact_with_local_structured_property():
    guido = ContactWithLocalStructuredProperty(
        name='Guido',
        addresses=[
            Address(
                type='home',
                city='Amsterdam'),
            Address(
                type='work',
                street='Spear St',
                city='SF')])

    guido.put()
    return guido


class SomeEntity(ndb.Model):
    name = ndb.StringProperty()
    name_lower = ndb.ComputedProperty(lambda self: self.name.lower())


def create_some_entity():
    entity = SomeEntity(name='Nick')
    entity.put()
    return entity


class Note(messages.Message):
    text = messages.StringField(1, required=True)
    when = messages.IntegerField(2)


class NoteStore(ndb.Model):
    note = msgprop.MessageProperty(Note, indexed_fields=['when'])
    name = ndb.StringProperty()


def create_note_store():
    my_note = Note(text='Excellent note', when=50)

    ns = NoteStore(note=my_note, name='excellent')
    key = ns.put()

    new_notes = NoteStore.query(NoteStore.note.when >= 10).fetch()
    return new_notes, key


class Notebook(messages.Message):
    notes = messages.MessageField(Note, 1, repeated=True)


class SignedStorableNotebook(ndb.Model):
    author = ndb.StringProperty()
    nb = msgprop.MessageProperty(
        Notebook, indexed_fields=['notes.text', 'notes.when'])


class Color(messages.Enum):
    RED = 620
    GREEN = 495
    BLUE = 450


class Part(ndb.Model):
    name = ndb.StringProperty()
    color = msgprop.EnumProperty(Color, required=True)


def print_part():
    p1 = Part(name='foo', color=Color.RED)
    print p1.color  # prints "RED"
