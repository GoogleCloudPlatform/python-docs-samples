# Copyright 2015 Google Inc.
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
import random
import urllib

import flask

# [START gae_ndb_transactions_import]
from google.appengine.api import taskqueue
from google.appengine.ext import ndb
# [END gae_ndb_transactions_import]


class Note(ndb.Model):
    """Models an individual Note entry with content."""

    content = ndb.StringProperty()


def parent_key(page_name):
    return ndb.Key("Parent", page_name)


app = flask.Flask(__name__)


@app.route("/")
def main_page():
    page_name = flask.request.args.get("page_name", "default")
    response = """
        <html><body>
            <h2>Permanent note page: %s</h2>""" % cgi.escape(
        page_name
    )

    parent = parent_key(page_name)
    notes = Note.query(ancestor=parent).fetch(20)
    for note in notes:
        response += "<h3>%s</h3>" % cgi.escape(note.key.id())
        response += "<blockquote>%s</blockquote>" % cgi.escape(note.content)

    response += """<hr>
           <form action="/add?%s" method="post">
           Submit Note: <input value="Title" name="note_title"><br>
           <textarea value="Note" name="note_text" rows="4" cols="60">
           </textarea>
           <input type="submit" value="Etch in stone"></form>""" % urllib.urlencode(
        {"page_name": page_name}
    )
    response += """
            <hr>
            <form>Switch page: <input value="%s" name="page_name">
            <input type="submit" value="Switch"></form>
            </body>
        </html>""" % cgi.escape(
        page_name, quote=True
    )

    return response


# [START gae_ndb_transactions_insert_standard]
@ndb.transactional
def insert_if_absent(note_key, note):
    fetch = note_key.get()
    if fetch is None:
        note.put()
        return True
    return False
# [END gae_ndb_transactions_insert_standard]


# [START gae_ndb_transactions_insert_two_tries]
@ndb.transactional(retries=1)
def insert_if_absent_2_retries(note_key, note):
    # do insert
    # [END gae_ndb_transactions_insert_two_tries]
    fetch = note_key.get()
    if fetch is None:
        note.put()
        return True
    return False


# [START gae_ndb_transactions_insert_cross_group]
@ndb.transactional(xg=True)
def insert_if_absent_xg(note_key, note):
    # do insert
    # [END gae_ndb_transactions_insert_cross_group]
    fetch = note_key.get()
    if fetch is None:
        note.put()
        return True
    return False


# [START gae_ndb_transactions_insert_sometimes]
def insert_if_absent_sometimes(note_key, note):
    # do insert
    # [END gae_ndb_transactions_insert_sometimes]
    fetch = note_key.get()
    if fetch is None:
        note.put()
        return True
    return False


# [START gae_ndb_transactions_insert_independent]
@ndb.transactional(propagation=ndb.TransactionOptions.INDEPENDENT)
def insert_if_absent_indep(note_key, note):
    # do insert
    # [END gae_ndb_transactions_insert_independent]
    fetch = note_key.get()
    if fetch is None:
        note.put()
        return True
    return False


# [START gae_ndb_transactions_insert_task_queue]
@ndb.transactional
def insert_if_absent_taskq(note_key, note):
    taskqueue.add(url=flask.url_for("taskq_worker"), transactional=True)
    # do insert
    # [END gae_ndb_transactions_insert_task_queue]
    fetch = note_key.get()
    if fetch is None:
        note.put()
        return True
    return False


@app.route("/worker")
def taskq_worker():
    pass


def pick_random_insert(note_key, note):
    choice = random.randint(0, 5)
    if choice == 0:
        # [START gae_ndb_transactions_insert_standard_calling_2]
        inserted = insert_if_absent(note_key, note)
        # [END gae_ndb_transactions_insert_standard_calling_2]
    elif choice == 1:
        inserted = insert_if_absent_2_retries(note_key, note)
    elif choice == 2:
        inserted = insert_if_absent_xg(note_key, note)
    elif choice == 3:
        # [START gae_ndb_transactions_insert_sometimes_callback]
        inserted = ndb.transaction(lambda: insert_if_absent_sometimes(note_key, note))
        # [END gae_ndb_transactions_insert_sometimes_callback]
    elif choice == 4:
        inserted = insert_if_absent_indep(note_key, note)
    elif choice == 5:
        inserted = insert_if_absent_taskq(note_key, note)
    return inserted


@app.route("/add", methods=["POST"])
def add_note():
    page_name = flask.request.args.get("page_name", "default")
    note_title = flask.request.form["note_title"]
    note_text = flask.request.form["note_text"]

    parent = parent_key(page_name)

    choice = random.randint(0, 1)
    if choice == 0:
        # Use transactional function
        # [START gae_ndb_transactions_insert_standard_calling_1]
        note_key = ndb.Key(Note, note_title, parent=parent)
        note = Note(key=note_key, content=note_text)
        # [END gae_ndb_transactions_insert_standard_calling_1]
        if pick_random_insert(note_key, note) is False:
            return 'Already there<br><a href="%s">Return</a>' % flask.url_for(
                "main_page", page_name=page_name
            )
        return flask.redirect(flask.url_for("main_page", page_name=page_name))
    elif choice == 1:
        # Use get_or_insert, which is transactional
        note = Note.get_or_insert(note_title, parent=parent, content=note_text)
        if note.content != note_text:
            return 'Already there<br><a href="%s">Return</a>' % flask.url_for(
                "main_page", page_name=page_name
            )
        return flask.redirect(flask.url_for("main_page", page_name=page_name))
