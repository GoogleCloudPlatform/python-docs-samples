## App Engine to App Engine Request Sample

This sample application shows how an App Engine for Python 3.7 app can make
a request to an App Engine for Python 2.7 app that includes an Authorization
header the receiving app can use to verify the calling app's identity.

This is a way for App Engine app-to-app requests can verify the identity of
the calling applications, replacing the built-in X-Appengine-Inbound-Appid
trustworthy header provided when using `urlfetch` in App Engine for
Python 2.7. It requires the receiving app to validate the incoming request
as shown in the appengine/standard/migration/incoming sample app in this
repository.

This sample app presents users with a form to fill in another App Engine
app's URL. On submission, this app calls the second App Engine app, and
echoes the response, as plain text, to the user.
