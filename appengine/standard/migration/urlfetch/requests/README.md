## App Engine simple urlfetch Replacement

The runtime for App Engine standard for Python 3 includes the `urlfetch`
library, which is used to make HTTP(S) requests. There are several related
capabilities provided by that library:

* Straightforward web requests
* Asynchronous web requests
* Platform authenticated web requests to other App Engine apps

The sample in this directory provides a way to make straightforward web requests
using only generally available Python libraries that work in either App Engine
standard for Python runtime, version 3.7.

To deploy and run this sample in App Engine standard for Python 3.7:

    gcloud app deploy app3.yaml
