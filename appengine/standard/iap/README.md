# Identity-Aware Proxy Refresh Session Sample

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=appengine/standard/iap/README.md

This sample is used on the following documentation page:

* https://cloud.google.com/iap/docs/sessions-howto


## Deploy to Google App Engine standard environment

```shell
$ gcloud app deploy

```

Enable Cloud IAP using the instructions here:
https://cloud.google.com/iap/docs/app-engine-quickstart#enabling_iap

## Usage

The app will continually refresh a fake status (always "Success"). After 1 hour,
the AJAX request will fail. The [js/poll.js](js/poll.js) code will detect this
and allow the user to refresh the session.
