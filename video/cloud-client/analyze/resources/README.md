# Resources folder for local files

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=video/cloud-client/analyze/resources/README.md

Copy from Google Cloud Storage to this folder for testing video analysis
of local files. For `cat.mp4` used in the usage example, run the following
`gcloud` command.

    gsutil cp gs://demomaker/cat.mp4 .

Now, when you run the following command, the video used for label detection
will be passed from here:

    python analyze.py labels_file resources/cat.mp4
