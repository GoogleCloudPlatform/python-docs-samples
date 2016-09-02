import webapp2
import update_schema
import jinja2
import os
from google.appengine.ext import deferred
import time

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class UpdateHandler(webapp2.RequestHandler):
    def get(self):
        current_entities = update_schema.get_current_entities()
        template_values = {
            'current_entities': current_entities,
            'updated_schema': False,
        }
        template = JINJA_ENVIRONMENT.get_template('home.html')
        self.response.write(template.render(template_values))

    def post(self):
        deferred.defer(update_schema.UpdateSchema)
        time.sleep(1)
        current_entities = update_schema.get_current_entities()
        template_values = {
            'current_entities': current_entities,
            'updated_schema': True,
        }
        template = JINJA_ENVIRONMENT.get_template('home.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([('/update_schema', UpdateHandler),])
