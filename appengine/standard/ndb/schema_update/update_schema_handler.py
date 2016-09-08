import os
import time

from google.appengine.ext import deferred
import jinja2

import update_schema
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class UpdateHandler(webapp2.RequestHandler):

    def post(self):
        deferred.defer(update_schema.update_schema)
        time.sleep(1)
        self.redirect('/display_entities?updated=true')

app = webapp2.WSGIApplication([('/update_schema', UpdateHandler), ])
