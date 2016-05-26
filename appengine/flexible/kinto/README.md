# Kinto Example

This is a basic example of running Mozillas [Kinto](https://github.com/Kinto/kinto/blob/master/docs/index.rst)
on App Engine Flexible. Kinto provides a framework to sync JSON data across many devices and provide push notifications.
This example uses a custom runtime to install Kinto and edit the config to run it on port 8080, which is the port that
the base Docker image is expecting. 

Since Kinto is being imported as a Python library and run as-is, no additional code is necessary.

Note that this is using Kinto's basic in-memory backend. As such, the instances are tied to 1. A production
version of Kinto would use a PostgreSQL database and Redis cluster, which would allow scaling to many instances.

If you are interested in seeing this example expanded to use PostgreSQL, you can file an Issue on the Issue
Tracker, or submit a Pull Request if you've accomplished it yourself.
 



