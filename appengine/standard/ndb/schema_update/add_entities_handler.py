import os
import time

import jinja2
import webapp2

import update_schema


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class AddEntitiesHandler(webapp2.RequestHandler):
    def post(self):
        author1 = self.request.get('author1', 'bob')
        name1 = self.request.get('name1', 'bob')
        author2 = self.request.get('author2', 'bob')
        name2 = self.request.get('name2', 'bob')
        update_schema.add_entity(author1, name1)
        update_schema.add_entity(author2, name2)
        time.sleep(1)
        current_entities = update_schema.get_current_entities(False)
        template_values = {
            'current_entities': current_entities,
            'updated_schema': False,
        }
        template = JINJA_ENVIRONMENT.get_template('home.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([('/add_entities', AddEntitiesHandler),])
