## App Engine to App Engine Request Sample

This sample application shows how an App Engine for Python 2.7 app can verify
the caller's identity for a request from an App Engine for Python 2.7 or
App Engine for Python 3.7 app.

Requests from an App Engine for Python 2.7 app that use `urlfetch` have
a trustworthy `X-Appengine-Inbound-Appid` header that can be used to verify
the calling app's identity.

Requests from an App Engine for Python 3.7 app that include an Authorization
header with an ID token for the calling app's default service account can
be used to verify those calling apps' identities.

The appengine/standard_python37/migration/urlfetch sample app can be used
to make calls to this app with a valid Authorization header.
