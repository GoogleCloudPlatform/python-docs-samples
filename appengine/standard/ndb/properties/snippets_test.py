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

import snippets


def test_account(testbed):
    account = snippets.Account(
        username='flan',
        userid=123,
        email='flan@example.com')
    account.put()


def test_employee(testbed):
    employee = snippets.Employee(
        full_name='Hob Gadling',
        retirement_age=600)
    employee.put()


def test_article(testbed):
    article = snippets.create_article()
    if article.title != 'Python versus Ruby':
        raise AssertionError
    if article.stars != 3:
        raise AssertionError
    if sorted(article.tags) != sorted(['python', 'ruby']):
        raise AssertionError


def test_create_contact(testbed):
    guido = snippets.create_contact()
    if guido.name != 'Guido':
        raise AssertionError
    addresses = guido.addresses
    if addresses[0].type != 'home':
        raise AssertionError
    if addresses[1].type != 'work':
        raise AssertionError
    if addresses[0].street is not None:
        raise AssertionError
    if addresses[1].street != 'Spear St':
        raise AssertionError
    if addresses[0].city != 'Amsterdam':
        raise AssertionError
    if addresses[1].city != 'SF':
        raise AssertionError


def test_contact_with_local_structured_property(testbed):
    guido = snippets.create_contact_with_local_structured_property()
    if guido.name != 'Guido':
        raise AssertionError
    addresses = guido.addresses
    if addresses[0].type != 'home':
        raise AssertionError
    if addresses[1].type != 'work':
        raise AssertionError


def test_create_some_entity(testbed):
    entity = snippets.create_some_entity()
    if entity.name != 'Nick':
        raise AssertionError
    if entity.name_lower != 'nick':
        raise AssertionError


def test_computed_property(testbed):
    entity = snippets.create_some_entity()
    entity.name = 'Nick'
    if entity.name_lower != 'nick':
        raise AssertionError
    entity.name = 'Nickie'
    if entity.name_lower != 'nickie':
        raise AssertionError


def test_create_note_store(testbed):
    note_stores, _ = snippets.create_note_store()
    if len(note_stores) != 1:
        raise AssertionError
    if note_stores[0].name != 'excellent':
        raise AssertionError
    if note_stores[0].name != 'excellent':
        raise AssertionError
    if note_stores[0].note.text != 'Excellent note':
        raise AssertionError
    if note_stores[0].note.when != 50:
        raise AssertionError


def test_notebook(testbed):
    note1 = snippets.Note(
        text='Refused to die.',
        when=1389)
    note2 = snippets.Note(
        text='Printed some things',
        when=1489)
    note3 = snippets.Note(
        text='Learned to use a sword',
        when=1589)

    notebook = snippets.Notebook(
        notes=[note1, note2, note3])
    stored_notebook = snippets.SignedStorableNotebook(
        author='Hob Gadling',
        nb=notebook)

    stored_notebook.put()


def test_part(testbed, capsys):
    snippets.print_part()
    stdout, _ = capsys.readouterr()
    if stdout.strip() != 'RED':
        raise AssertionError
