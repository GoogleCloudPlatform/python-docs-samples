# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Sample application that shows how to perform a "schema migration" using
Google Cloud Datastore.

This application uses one model named "Pictures" but two different versions
of it. v2 contains two extra fields. The application shows how to
populate these new fields onto entities that existed prior to adding the
new fields to the model class.
"""
# [START imports]
import logging
import os

from google.appengine.ext import deferred
from google.appengine.ext import ndb
import jinja2
import webapp2

import models_v1
import models_v2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]


# [START display_entities]
class DisplayEntitiesHandler(webapp2.RequestHandler):
    """Displays the current set of entities and options to add entities
    or update the schema."""
    def get(self):
        # Force ndb to use v2 of the model by re-loading it.
        reload(models_v2)

        entities = models_v2.Picture.query().fetch()
        template_values = {
            'entities': entities,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END display_entities]


# [START add_entities]
class AddEntitiesHandler(webapp2.RequestHandler):
    """Adds new entities using the v1 schema."""
    def post(self):
        # Force ndb to use v1 of the model by re-loading it.
        reload(models_v1)

        # Save some example data.
        ndb.put_multi([
            models_v1.Picture(author='Alice', name='Sunset'),
            models_v1.Picture(author='Bob', name='Sunrise')
        ])

        self.response.write("""
        Entities created. <a href="/">View entities</a>.
        """)
# [END add_entities]


# [START update_schema]
class UpdateSchemaHandler(webapp2.RequestHandler):
    """Queues a task to start updating the model schema."""
    def post(self):
        deferred.defer(update_schema_task)
        self.response.write("""
        Schema update started. Check the console for task progress.
        <a href="/">View entities</a>.
        """)


def update_schema_task(cursor=None, num_updated=0, batch_size=100):
    """Task that handles updating the models' schema.

    This is started by
    UpdateSchemaHandler. It scans every entity in the datastore for the
    Picture model and re-saves it so that it has the new schema fields.
    """

    # Force ndb to use v2 of the model by re-loading it.
    reload(models_v2)

    # Get all of the entities for this Model.
    query = models_v2.Picture.query()
    pictures, next_cursor, more = query.fetch_page(
        batch_size, start_cursor=cursor)

    to_put = []
    for picture in pictures:
        # Give the new fields default values.
        # If you added new fields and were okay with the default values, you
        # would not need to do this.
        picture.num_votes = 1
        picture.avg_rating = 5
        to_put.append(picture)

    # Save the updated entities.
    if to_put:
        ndb.put_multi(to_put)
        num_updated += len(to_put)
        logging.info(
            'Put {} entities to Datastore for a total of {}'.format(
                len(to_put), num_updated))

    # If there are more entities, re-queue this task for the next page.
    if more:
        deferred.defer(
            update_schema_task, cursor=next_cursor, num_updated=num_updated)
    else:
        logging.debug(
            'update_schema_task complete with {0} updates!'.format(
                num_updated))
# [END update_schema]


app = webapp2.WSGIApplication([
    ('/', DisplayEntitiesHandler),
    ('/add_entities', AddEntitiesHandler),
    ('/update_schema', UpdateSchemaHandler)])
