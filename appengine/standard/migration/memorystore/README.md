## App Engine Memorystore for Redis Sample

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=appengine/standard/migration/memorystore/README.md

This is a sample app for Google App Engine that demonstrates how to replace
use of the [Memcache API](https://cloud.google.com/appengine/docs/standard/python/memcache)
with the [Memorystore for Redis offering](https://cloud.google.com/memorystore).
This newer library can be used on App Engine with either Python 2.7
or Python 3.

Code taken from the [Memcache sample](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/appengine/standard/memcache/snippets/snippets.py)
is included in this new sample, with each line commented out with two # marks.
This allows the older solution's approach to be contrasted with the
Memorystore for Redis approach.

Prior to deploying this sample, a
[serverless VPC connector](https://cloud.google.com/vpc/docs/configure-serverless-vpc-access)
must be created and then a
[Memorystore for Redis instance](https://cloud.google.com/memorystore/docs/redis/quickstart-console)
on the same VPC. The IP address and port number of the Redis instance, and
the name of the VPC connector should be entered in either app.yaml
(for Python 2.7) or app3.yaml (for Python 3).

To deploy and run this sample in App Engine standard for Python 2.7:

    pip install -t lib -r requirements.txt
    gcloud app deploy

To deploy and run this sample in App Engine standard for Python 3.7:

    gcloud app deploy app3.yaml
    