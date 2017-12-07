# Using Background Threads from Google App Engine

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=appengine/standard/background/README.md

This example shows how to use manual or basic scaling to start App Engine background threads.

See the [documentation on modules](https://cloud.google.com/appengine/docs/python/modules/) for
more information.

Your app.yaml configuration must specify scaling as either manual or basic. The default 
automatic scaling does not allow background threads.
