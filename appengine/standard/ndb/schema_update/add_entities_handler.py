import os

import jinja2
import webapp2
from google.appengine.ext import ndb

import models_v1

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class AddEntitiesHandler(webapp2.RequestHandler):
    def post(self):
        # Re-imports the models_v1 module so its Picture class replaces the
        # current class
        reload(models_v1)
        ndb.put_multi([
            models_v1.Picture(author='Alice', name='Sunset'),
            models_v1.Picture(author='Bob', name='Sunrise')
        ])
        # time.sleep(1) - Eventual consistency issue with entities
        self.redirect('/display_entities')

app = webapp2.WSGIApplication([('/add_entities', AddEntitiesHandler), ])
