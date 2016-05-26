#!/usr/bin/env python

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

import logging

from google.appengine.api import memcache
from google.appengine.ext import ndb
import webapp2


# [START best-practice-2]
class Person(ndb.Model):
    name = ndb.StringProperty(required=True)
    userid = ndb.StringProperty(required=True)


def get_or_add_person(name, userid):
    person = memcache.get(name)
    if person is None:
        person = Person(name=name, userid=userid)
        memcache.add(name, person)
    else:
        logging.info('Found in cache: ' + name + ', userid: ' + person.userid)
    return person
# [END best-practice-2]


class MainPage(webapp2.RequestHandler):
    def get(self):
        person = get_or_add_person('Stevie Wonder', "1")
        self.response.content_type = 'text/html'
        self.response.write(person.name)


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
