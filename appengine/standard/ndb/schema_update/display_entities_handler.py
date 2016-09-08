import os

import jinja2
import webapp2

import models_v1
import models_v2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def get_current_entities(updated_schema=False):
    if updated_schema:
        reload(models_v2)
        current_entities = list(models_v2.Picture.query().fetch())
    else:
        reload(models_v1)
        current_entities = list(models_v1.Picture.query().fetch())
    return current_entities


class DisplayEntitiesHandler(webapp2.RequestHandler):
    def get(self):
        updated_schema = self.request.params.get('updated')
        if updated_schema is None:
            updated_schema = False
        else:
            updated_schema = True
        current_entities = get_current_entities(updated_schema)
        template_values = {
            'current_entities': current_entities,
            'updated_schema': updated_schema,
        }
        template = JINJA_ENVIRONMENT.get_template('home.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([('/display_entities', DisplayEntitiesHandler),
                               ])
