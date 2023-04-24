# Access legacy bundled Mail API in Python 3

This app receives mail and logs its content, and sends mail messages as well.
When run in App Engine, a GET request to the home page (`/` path) will display
a page with a form for entering an email address and a text message.

You can send a message to an address associated with the app (in the form
`somename@[CLOUD_PROJECT_ID].appspotmail.com`, where CLOUD_PROJECT_ID is
the project ID the app is running in) and later view
the received message in the log. Or you can send to a nonexistent address such
as `nobody@example.com` and then view the bounced message in the log.

In order to receive incoming email, the `app.yaml` file must specify `mail` and
`mail_bounce` as `inbound_services`.

Deploy this app to App Engine via `gcloud app deploy`. More about App Engine
Bundled Mail API at:
https://cloud.google.com/appengine/docs/standard/python3/services/mail#python-3-flask
