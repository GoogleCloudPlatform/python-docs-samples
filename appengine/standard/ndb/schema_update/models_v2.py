from google.appengine.ext import ndb


class Picture(ndb.Model):
    author = ndb.StringProperty()
    name = ndb.StringProperty(default='')  # Unique name.
    num_votes = ndb.IntegerProperty(default=0)
    avg_rating = ndb.FloatProperty(default=0)
