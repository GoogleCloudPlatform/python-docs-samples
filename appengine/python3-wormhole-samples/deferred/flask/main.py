from flask import Flask, request
from google.appengine.api import wrap_wsgi_app
from google.appengine.ext import ndb
from google.appengine.ext import deferred

my_key = 'main'


app = Flask(__name__)
app.wsgi_app = wrap_wsgi_app(app.wsgi_app, use_deferred=True)


class Counter(ndb.Model):
    count = ndb.IntegerProperty(indexed=False)


def do_something_later(key, amount):
      entity = Counter.get_or_insert(key, count=0)
      entity.count += amount
      entity.put()


@app.route("/counter/increment")
def increment_counter():
  # Use default URL and queue name, no task name, execute ASAP.
  deferred.defer(do_something_later, my_key, 20)

  # Use default URL and queue name, no task name, execute after 60s.
  deferred.defer(do_something_later, my_key, 20, _countdown=60)

  # Providing non-default task queue arguments
  deferred.defer(do_something_later, my_key, 20, _url='/custom/path', _countdown=60)

  return 'Deferred counter increment.'


@app.route("/counter/get")
def view_counter():
  counter = Counter.get_or_insert(my_key, count=0)
  return str(counter.count)


@app.route("/custom/path", methods=['POST'])
def custom_deferred():
  print("Executing deferred task.")
  # request.environ contains the WSGI `environ` dictionary (See PEP 0333)
  return deferred.Handler().post(request.environ)