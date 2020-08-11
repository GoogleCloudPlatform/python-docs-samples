# Copyright 2020 Google LLC
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

# [START all]
from flask import Flask, redirect, render_template, request
from google.cloud import ndb
import logging

try:
    from urllib import urlencode
except Exception:
    from urllib.parse import urlencode

app = Flask(__name__)
client = ndb.Client()

try:
    global_cache = ndb.RedisCache.from_environment()
except Exception:
    logging.warning('Redis not available.')
    global_cache = None


# [START greeting]
class Greeting(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
# [END greeting]

# [START query]
    with client.context(global_cache=global_cache):
        @classmethod
        def query_book(cls, ancestor_key):
            return cls.query(ancestor=ancestor_key).order(-cls.date)


@app.route('/', methods=['GET'])
def display_guestbook():
    guestbook_name = request.args.get('guestbook_name', '')
    print('GET guestbook name is {}'.format(guestbook_name))
    with client.context(global_cache=global_cache):
        ancestor_key = ndb.Key("Book", guestbook_name or "*notitle*")
        greetings = Greeting.query_book(ancestor_key).fetch(20)
# [END query]

    greeting_blockquotes = [greeting.content for greeting in greetings]
    return render_template(
            'index.html',
            greeting_blockquotes=greeting_blockquotes,
            guestbook_name=guestbook_name
        )


# [START submit]
@app.route('/sign', methods=['POST'])
def update_guestbook():
    # We set the parent key on each 'Greeting' to ensure each guestbook's
    # greetings are in the same entity group.
    guestbook_name = request.form.get('guestbook_name', '')
    print('Guestbook name from the form: {}'.format(guestbook_name))

    with client.context(global_cache=global_cache):
        print('Guestbook name from the URL: {}'.format(guestbook_name))
        greeting = Greeting(
                parent=ndb.Key("Book", guestbook_name or "*notitle*"),
                content=request.form.get('content', None)
            )
        greeting.put()
# [END submit]

    return redirect('/?' + urlencode({'guestbook_name': guestbook_name}))


if __name__ == '__main__':
    # This is used when running locally.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END all]
