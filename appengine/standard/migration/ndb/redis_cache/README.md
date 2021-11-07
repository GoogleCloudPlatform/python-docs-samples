## App Engine Datastore NDB Overview Sample

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=appengine/standard/migration/ndb/overview/README.md

This is a sample app for Google App Engine that demonstrates how to replace
use of the [Datastore NDB Python API](https://cloud.google.com/appengine/docs/python/ndb/)
with the [Google Cloud NDB library](https://googleapis.dev/python/python-ndb/latest/index.html).
This library can be used not only on App Engine, but also other Python 3
platforms.

This sample also uses
[Memorystore for Redis](https://cloud.google.com/memorystore/docs/redis/redis-overview)
caching to improve NDB performance in some situations.

Prior to deploying this sample, a
[serverless VPC connector](https://cloud.google.com/vpc/docs/configure-serverless-vpc-access)
must be created and then a
[Memorystore for Redis instance](https://cloud.google.com/memorystore/docs/redis/quickstart-console)
on the same VPC. The IP address and port number of the Redis instance, and
the name of the VPC connector should be entered in either app.yaml
(for Python 2.7) or app3.yaml (for Python 3).

To deploy and run this sample in App Engine standard for Python 2.7:

    pip install -t lib -r requirements.txt
    gcloud app deploy app.yaml index.yaml

To deploy and run this sample in App Engine standard for Python 3.7:

    gcloud app deploy app3.yaml index.yaml
