# Copyright 2015 Google Inc. All rights reserved.
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

import cgi
import flask
import random
import urllib
from google.appengine.ext import ndb


class Note(ndb.Model):
    """Models an individual Note entry with content."""
    content = ndb.StringProperty()


def parent_key(page_name):
    return ndb.Key("Parent", page_name)


app = flask.Flask(__name__)


@app.route('/')
def main_page():
    page_name = flask.request.args.get('page_name', 'default')
    response = """
        <html><body>
            <h2>Permenant note page: %s</h2>""" % cgi.escape(page_name)

    parent = parent_key(page_name)
    notes = Note.query(ancestor=parent).fetch(20)
    for note in notes:
        response += '<h3>%s</h3>' % cgi.escape(note.key.id())
        response += '<blockquote>%s</blockquote>' % cgi.escape(note.content)

    response += """
            <hr>
            <form action="/add?%s" method="post">
            Submit Note: <input value="Title" name="note_title"><br>
            <textarea value="Note" name="note_text" rows="4" cols="60"></textarea>
            <input type="submit" value="Etch in stone"></form>""" % urllib.urlencode({'page_name': page_name})
    response += """
            <hr>
            <form>Switch page: <input value="%s" name="page_name">
            <input type="submit" value="Switch"></form>
            </body>
        </html>""" % cgi.escape(page_name, quote=True)

    return response


# [START standard]
@ndb.transactional
def insert_if_absent(note_key, note):
    fetch = note_key.get()
    if fetch is None:
        note.put()
        return True
    return False
# [END standard]


# [START two-tries]
@ndb.transactional(retries=1)
def insert_if_absent_2_retries(note_key, note):
    # [END two-tries]
    fetch = note_key.get()
    if fetch is None:
        note.put()
        return True
    return False


# [START cross-group]
@ndb.transactional(xg=True)
def insert_if_absent_xg(note_key, note):
    # [END cross-group]
    fetch = note_key.get()
    if fetch is None:
        note.put()
        return True
    return False


# [START sometimes]
def insert_if_absent_sometimes(note_key, note):
    # [END sometimes]
    fetch = note_key.get()
    if fetch is None:
        note.put()
        return True
    return False


# [START indep]
@ndb.transactional(propagation=ndb.TransactionOptions.INDEPENDENT)
def insert_if_absent_indep(note_key, note):
    # [END indep]
    fetch = note_key.get()
    if fetch is None:
        note.put()
        return True
    return False


def pick_random_insert(note_key, note):
    choice = random.randint(0, 4)
    if choice == 0:
        # [START calling2]
        return insert_if_absent(note_key, note)
        # [END calling2]
    elif choice == 1:
        return insert_if_absent_2_retries(note_key, note)
    elif choice == 2:
        return insert_if_absent_xg(note_key, note)
    elif choice == 3:
        # [START sometimes-call]
        return ndb.transaction(lambda: insert_if_absent_sometimes(note_key, note))
        # [END sometimes-call]
    elif choice == 4:
        return insert_if_absent_indep(note_key, note)


@app.route('/add', methods=['POST'])
def add_note():
    page_name = flask.request.args.get('page_name', 'default')
    note_title = flask.request.form['note_title']
    note_text = flask.request.form['note_text']

    parent = parent_key(page_name)

    choice = random.randint(0, 1)
    if choice == 0:
        # Use transactional function
        # [START calling]
        note_key = ndb.Key(Note, note_title, parent=parent)
        note = Note(key=note_key, content=note_text)
        # [END calling]
        if pick_random_insert(note_key, note) is False:
            return 'Already there<br><a href="%s">Return</a>' % flask.url_for('main_page', page_name=page_name)
        return flask.redirect(flask.url_for('main_page', page_name=page_name))
    elif choice == 1:
        # Use get_or_insert, which is transactional
        note = Note.get_or_insert(note_title, parent=parent, content=note_text)
        if note.content != note_text:
            return 'Already there<br><a href="%s">Return</a>' % flask.url_for('main_page', page_name=page_name)
        return flask.redirect(flask.url_for('main_page', page_name=page_name))


if __name__ == '__main__':
    app.run()
