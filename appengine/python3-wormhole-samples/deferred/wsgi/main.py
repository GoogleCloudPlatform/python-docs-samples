from google.appengine.api import wrap_wsgi_app
from google.appengine.ext import ndb
from google.appengine.ext import deferred
import re

my_key = 'main'


class Counter(ndb.Model):
    count = ndb.IntegerProperty(indexed=False)

def do_something_later(key, amount):
      entity = Counter.get_or_insert(key, count=0)
      entity.count += amount
      entity.put()

def IncrementCounter(environ, start_response):
  # Use default URL and queue name, no task name, execute ASAP.
  deferred.defer(do_something_later, my_key, 20)

  # Use default URL and queue name, no task name, execute after 60s.
  deferred.defer(do_something_later, my_key, 20, _countdown=60)

  # Providing non-default task queue arguments
  deferred.defer(do_something_later, my_key, 20, _url='/custom/path', _countdown=60)

  start_response('200 OK', [('Content-Type', 'text/html')])
  return ['Deferred counter increment.'.encode('utf-8')]

def ViewCounter(environ, start_response):
  counter = Counter.get_or_insert(my_key, count=0)
  start_response('200 OK', [('Content-Type', 'text/html')])
  return [str(counter.count).encode('utf-8')]


class CustomDeferredHandler(deferred.Handler):
  """Deferred task handler that adds additional logic."""

  def post(self, environ):
      print("Executing deferred task.")
      return super().post(environ)

routes = {
          'counter/increment': IncrementCounter,
          'counter/get': ViewCounter,
          'custom/path': CustomDeferredHandler() 
          }


class WSGIApplication():
  def __call__(self, environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex, handler in routes.items():
      match = re.search(regex, path)
      if match is not None:
        return handler(environ, start_response)

app = wrap_wsgi_app(WSGIApplication(), use_deferred=True)