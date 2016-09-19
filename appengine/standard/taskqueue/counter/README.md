# App Engine Task Queue Counter

To run this app locally, specify both `.yaml` files to `dev_appserver.py`:

    dev_appserver.py -A your-app-id app.yaml worker.yaml

To deploy this application, specify both `.yaml` files to `appcfg.py`:

    appcfg.py update -A your-app-id -V 1 app.yaml worker.yaml

<!-- auto-doc-link -->
These samples are used on the following documentation pages:

>
* https://cloud.google.com/appengine/docs/python/taskqueue/push/creating-handlers
* https://cloud.google.com/appengine/docs/python/taskqueue/push/creating-tasks

<!-- end-auto-doc-link -->
