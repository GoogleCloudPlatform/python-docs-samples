# App Engine Task Queue Counter

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=appengine/standard/taskqueue/counter/README.md

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
