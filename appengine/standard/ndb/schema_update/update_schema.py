import logging

from google.appengine.ext import deferred
from google.appengine.ext import ndb

import models_v2

# ideal batch size may vary based on entity size.
BATCH_SIZE = 100


def update_schema(cursor=None, num_updated=0):
    # Re-imports the models_v2 module so its Picture class replaces the
    # current class
    reload(models_v2)
    query = models_v2.Picture.query()
    pictures, cursor, more = query.fetch_page(BATCH_SIZE, start_cursor=cursor)

    to_put = []
    for picture in pictures:
        # In this example, the default values of 0 for num_votes and avg_rating
        # are acceptable, so we don't need this loop.  If we wanted to manually
        # manipulate property values, it might go something like this:
        picture.num_votes = 1
        picture.avg_rating = 5
        to_put.append(picture)

    if to_put:
        ndb.put_multi(to_put)
        num_updated += len(to_put)
        logging.debug(
            'Put {0} entities to Datastore for a total of {1}'.format(
                len(to_put), num_updated))
    if more:
        deferred.defer(
            update_schema, cursor=query.cursor(), num_updated=num_updated)
    else:
        logging.debug(
            'UpdateSchema complete with {0} updates!'.format(num_updated))
