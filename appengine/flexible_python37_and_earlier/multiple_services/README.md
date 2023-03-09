# Python Google Cloud Microservices Example - API Gateway

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=appengine/flexible_python37_and_earlier/multiple_services/README.md

This example demonstrates how to deploy multiple python services to [App Engine flexible environment](https://cloud.google.com/appengine/docs/flexible/)

## To Run Locally

Open a terminal and start the first service:

```Bash
$ cd gateway-service
$ # follow https://cloud.google.com/python/docs/setup to set up a Python
development environment
$ pip install -r requirements.txt
$ python main.py
```

In a separate terminal, start the second service:

```Bash
$ cd static-service
$ # follow https://cloud.google.com/python/docs/setup to set up a Python
$ pip install -r requirements.txt
$ python main.py
```

## To Deploy to App Engine

### YAML Files

Each directory contains an `app.yaml` file.  These files all describe a
separate App Engine service within the same project.

For the gateway:

[Gateway service <default>](gateway/app.yaml)

This is the `default` service.  There must be one (and not more).  The deployed
url will be `https://<your project id>.appspot.com`

For the static file server:

[Static file service <static>](static/app.yaml)

The deployed url will be `https://<service name>-dot-<your project id>.appspot.com`

### Deployment

To deploy a service cd into its directory and run:
```Bash
$ gcloud app deploy app.yaml
```
and enter `Y` when prompted.  Or to skip the check add `-q`.

To deploy multiple services simultaneously just add the path to each `app.yaml`
file as an argument to `gcloud app deploy `:
```Bash
$ gcloud app deploy gateway-service/app.yaml static-service/app.yaml
```
