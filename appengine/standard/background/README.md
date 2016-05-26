# Using Background Threads from Google App Engine

This example shows how to use manual or basic scaling to start App Engine background threads.

See the [documentation on modules](https://cloud.google.com/appengine/docs/python/modules/) for
more information.

Your app.yaml configuration must specify scaling as either manual or basic. The default 
automatic scaling does not allow background threads.
