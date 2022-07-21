# Access bundled Deferred services API in Python 3

This folder contains functionally identical apps that illustrate
use of the App Engine Deferred service.

The apps are written using three different web frameworks:
[Flask](https://palletsprojects.com/p/flask/),
[Django](https://www.djangoproject.com/), and the [App Engine bundled services
wsgi functionality](https://github.com/GoogleCloudPlatform/appengine-python-standard).

When run in App Engine, a GET request to `/counter/get` will display the
current value of the counter. A GET request to `/counter/increment` will
cause the counter to be incremented via the Deferred service, once immediately,
once after 10 seconds, and once after 20 seconds.

Deploy this app to App Engine via `gcloud app deploy`. More about App Engine
Bundled Deferred API at:
https://cloud.google.com/appengine/docs/standard/python3/services/deferred#python-3-flask

## Testing

The App Engine bundled services can be used from within properly configured App
Engine applications, so testing these apps requires deploying them to App Engine.

Each version of the app includes a test program that will:

1. Launch a new version of the app to App Engine without routing network
requests to it.
1. Interact with the launched app via web requests to the URL of the
specific version that was launched.
1. Delete the newly launched app version. This is possible because it did not
have requests routed to it.

Since each test uses a separate version and addresses test messages and web
requests to that version, multiple tests can run simultaneously without
interfering with each other.
