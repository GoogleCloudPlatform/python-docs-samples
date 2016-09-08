from google.appengine.ext import ndb


class Picture(ndb.Model):
    author = ndb.StringProperty()
    name = ndb.StringProperty(default='')  # Unique name.
