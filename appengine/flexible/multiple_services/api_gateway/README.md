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

4. Change the url's in the API gateway `gateway/api_gateway.py` to the
development ports specified in line `gateway/api_gateway.py:6`
```Python
development ports {static: 8003, flask1: 8001, flask2: 8002}
```

## To Deploy to App Engine

### YAML Files

Each directory contains an `app.yaml file`.  This file will be the same as if
each service were its own project except for the `service` line. For the gateway:

[Gateway <default>](gateway/app.yaml)

This is the `default` service.  There must be one (and not more).  The deployed
url will be `https://<your project id>.appspot.com`

For the other services:

[Flask Server 1 <flask1>](flask/app.yaml)
[Flask Server 2 <flask2](flask2/app.yaml)
[Static File Server <static>](static/app.yaml)

Make sure the `entrypoint` line matches the filename of the server you want to deploy.

The deployed url will be `https://<service name>-dot-<your project id>.appspot.com`

### Deployment

To deploy a service cd into its directory and run: `gcloud app deploy app.yaml`
and enter `Y` when prompted.  Or to skip the check add `-q`.

Recommend deploying the `static`, `flask1`, and `flask2` services first and
then filling in the correct service urls into the gateway before deployment.

To test if a service is successfully deployed, simply navigate to the root
and you will see a message.  
