# Python Google Cloud Microservices Example - API Gateway

This example demonstrates how to deploy multiple python services to [App Engine Flexible Environment](https://cloud.google.com/appengine/docs/flexible/)

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

5. To run each server locally:
```Bash
$ source env/bin/activate
$ export FLASK_DEBUG=1 #optional to run in debug mode
$ python <server name>.py development
$ deactivate #after shutting down server
```

## To Deploy to App Engine

### YAML Files

Each directory contains an `app.yaml file`.  This file will be the same as if
each service were its own project except for the `service` line. For the gateway:
```YAML
service: default
runtime: python
vm: true
entrypoint: gunicorn -b :$PORT api_gateway:app

runtime_config:
  python_version: 3
```  

This is the `default` service.  There must be one (and not more).  The deployed
url will be `https://<your project id>.appspot.com`

For one of the other services:

```YAML
service: <service name>
runtime: python
vm: true
entrypoint: gunicorn -b :$PORT flask_server:app

runtime_config:
  python_version: 3
```  

Make sure the `entrypoint` line matches the filename of the server you want to deploy.

The deployed url will be `https://<service name>-dot-<your project id>.appspot.com`

### Deployment

To deploy a service cd into its directory and run: `gcloud app deploy app.yaml`
and enter `Y` when prompted.  Or to skip the check add `-q`.

Recommend deploying the `static`, `flask1`, and `flask2` services first and
then filling in the correct service urls into the gateway before deployment.

To test if a service is successfully deployed, simply navigate to the root
and you will see a message.  
