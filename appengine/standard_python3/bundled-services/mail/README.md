# Access bundled Mail services API in Python 3

This folder contains functionally identical apps that each receive email
messages and log information about them. They each send email messages as well.
The apps are written using three different web frameworks:
[Flask](https://palletsprojects.com/p/flask/),
[Django](https://www.djangoproject.com/), and the [App Engine bundled services
wsgi functionality](https://github.com/GoogleCloudPlatform/appengine-python-standard).

When run in App Engine, a GET request to the home page (`/` path) will display
a page with a form for entering an email address and a text message. When the
form is submitted, the app will send a message with that text to the specified
address.

You can send a message to an address associated with the app (in the form
`somename@[CLOUD_PROJECT_ID].appspotmail.com`, where CLOUD_PROJECT_ID is
the project ID the app is running in, and `somename` can be any name you'd like)
and later view the received message in the log. Or you can send to a
nonexistent address such as `nobody@example.com` and then view the bounced
message in the log.

In order to receive incoming email, the `app.yaml` file must specify `mail` and
`mail_bounce` as `inbound_services`.

Deploy this app to App Engine via `gcloud app deploy`. More about App Engine
Bundled Mail API at:
https://cloud.google.com/appengine/docs/standard/python3/services/mail#python-3-flask

## Testing

The App Engine bundled services can be used from within properly configured App
Engine applications, and email messages are delivered to those applications,
so testing these apps requires deploying them to App Engine.

Each version of the app includes a test program that will:

1. Launch a new version of the app to App Engine without routing network
requests to it.
1. Interact with the launched app via web requests to the URL of the
specific version that was launched.
1. Examine the log messages of that version to see that the expected actions
worked and were logged.
1. Delete the newly launched app version. This is possible because it did not
have requests routed to it.

Since each test uses a separate version and addresses test messages and web
requests to that version, multiple tests can run simultaneously without
interfering with each other.

### Bounced messages limitation

Bounce notifications will be delivered only to the default App Engine version
that has requests routed to it. This means that they will never be delivered
to the temporary versions that the test code creates, and would have to
be tested another way, such as manually.
