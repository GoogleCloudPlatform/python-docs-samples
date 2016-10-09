# Python Google Cloud Microservices Example - API Gateway

This example demonstrates how to deploy multiple python services to [App Engine flexible environment](https://cloud.google.com/appengine/docs/flexible/)

## To Run Locally

1. You will need to install Python 3 on your local machine

2. Install virtualenv
```Bash
$ pip install virtualenv
```

3. To setup the environment in each server's directory:
```Bash
$ virtualenv -p python3 env
$ source env/bin/activate
$ pip install -r requirements.txt
$ deactivate
```

4. To start server locally:
```Bash
$ python <filename>.py
```

## To Deploy to App Engine

### YAML Files

Each directory contains an `app.yaml` file.  These files all describe a
separate App Engine service within the same project.

For the gateway:

[Gateway <default>](gateway/app.yaml)

This is the `default` service.  There must be one (and not more).  The deployed
url will be `https://<your project id>.appspot.com`

For the static file server:

[Static File Server <static>](static/app.yaml)

Make sure the `entrypoint` line matches the filename of the server you want to deploy.

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
$ gcloud app deploy gateway/app.yaml static/app.yaml
```
