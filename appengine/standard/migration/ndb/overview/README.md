## App Engine Datastore NDB Overview Sample

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=appengine/standard/migration/ndb/overview/README.md

This is a sample app for Google App Engine that demonstrates how to replace
use of the [Datastore NDB Python API](https://cloud.google.com/appengine/docs/python/ndb/)
with the [Google Cloud NDB library](https://googleapis.dev/python/python-ndb/latest/index.html).
This library can be used not only on App Engine, but also other Python 3
platforms.

To deploy and run this sample in App Engine standard for Python 2.7:

    pip install -t lib -r requirements.txt
    gcloud app deploy

To deploy and run this sample in App Engine standard for Python 3.7:

    gcloud app deploy app3.yaml
