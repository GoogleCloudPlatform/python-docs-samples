# Google Error Reorting Samples Samples

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=error_reporting/fluent_on_compute/README.md

This section contains samples for [Google Cloud Error Reporting](https://cloud.google.com/error-reporting).

A startup script has been provided to demonstrated how to properly provision a GCE 
instance with fluentd configured. Note the intallation of fluentd, the addition of the config file,
 and the restarting of the fluetnd service. You can start an instance  using
it like this:

    gcloud compute instances create example-instance --metadata-from-file startup-script=startup_script.sh

or simply use it as reference when creating your own instance.

After fluentd is configured, main.py could be used to simulate an error:

    gcloud compute copy-files main.py example-instance:~/main.py
   
Then, 

    gcloud compute ssh example-instance
    python ~/main.py
   
And you will see the message in the Errors Console.

<!-- auto-doc-link -->
These samples are used on the following documentation page:

> https://cloud.google.com/error-reporting/docs/setting-up-on-compute-engine

<!-- end-auto-doc-link -->
