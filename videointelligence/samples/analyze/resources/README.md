# Resources folder for local files

Copy from Google Cloud Storage to this folder for testing video analysis
of local files. For `cat.mp4` used in the usage example, run the following
`gcloud` command.

    gsutil cp gs://demomaker/cat.mp4 .

Now, when you run the following command, the video used for label detection
will be passed from here:

    python analyze.py labels_file resources/cat.mp4
