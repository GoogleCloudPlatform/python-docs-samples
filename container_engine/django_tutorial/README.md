# Getting started with Django on Google Container Engine

This repository is an example of how to run a [Django](https://www.djangoproject.com/) 
app on Google Container Engine. It uses the [Writing your first Django app](https://docs.djangoproject.com/en/1
.9/intro/tutorial01/) Polls application as the example app to deploy. From here on out, we refer to this app as
the 'polls' application.

## Pre-requisites

1. Create a project in the [Google Cloud Platform Console](https://console.cloud.google.com).

2. [Enable billing](https://console.cloud.google.com/project/_/settings) for your project.

3. [Enable APIs](https://console.cloud.google.com/flows/enableapi?apiid=datastore,pubsub,storage_api,logging,plus) for your project. The provided link will enable all necessary APIs, but if you wish to do so manually you will need Datastore, Pub/Sub, Storage, and Logging.

4. Install the [Google Cloud SDK](https://cloud.google.com/sdk)

        $ curl https://sdk.cloud.google.com | bash 
        $ gcloud init

5. Install [Docker](https://www.docker.com/).

## Makefile

Several commands listed below are provided in simpler form via the Makefile. Many of them use the GCLOUD_PROJECT 
environment variable, which will be picked up from your gcloud config. Make sure you set this to the correct project,

    gcloud config set project <your-project-id>

### Create a cluster

Create a cluster for the bookshelf application:

    gcloud container clusters create bookshelf \
        --scope "https://www.googleapis.com/auth/userinfo.email","cloud-platform" \
        --num-nodes 2
    gcloud container clusters get-credentials bookshelf

The scopes specified in the `--scope` argument allows nodes in the cluster to access Google Cloud Platform APIs, such as the Cloud Datastore API.

### Create a Cloud Storage bucket

The bookshelf application uses [Google Cloud Storage](https://cloud.google.com/storage) to store image files. Create a bucket for your project:

    gsutil mb gs://<your-project-id>
    gsutil defacl set public-read gs://<your-project-id>


## Setup the database

This tutorial assumes you are setting up Django using a SQL database, which is the easiest way to run Django. If you have an existing SQL database running, you can use that, but if not, these are the instructions for creating a managed MySQL instance using CloudSQL.


* Create a [CloudSQL instance](https://console.cloud.google.com/project/_/sql/create)

    * In the instances list, click your Cloud SQL instance.

    * Click Access Control.

    * In the IP address subsection, click Request an IPv4 address to enable access to the Cloud SQL instance through an 
    IPv4 address. It will take a moment to initialize the new IP address.

    * Also under Access Control, in the Authorization subsection, under Allowed Networks, click the add (+) button .

    * In the Networks field, enter 0.0.0.0/0. This value allows access by all IP addresses.

    * Click Save.

Note: setting allowed networks to 0.0.0.0/0 opens your SQL instance to traffic from any computer. For production databases, it's highly recommended to limit the authorized networks to only IP ranges that need  access.

* Alternatively, the instance can be created with the gcloud command line tool as follows, substituting `your-root-pw
 with a strong, unique password.

    `gcloud sql instances create <instance_name> --assign-ip --authorized-networks=0.0.0.0/0  set-root-password=your-root-pw`

* Create a Database And User

    * Using the root password created in the last step to create a new database, user, and password using your preferred MySQL client. Alternatively, follow these instructions to create the database and user from the console.
        * From the CloudSQL instance in the console,  click New user.
        * Enter a username and password for the application. For example, name the user "pythonapp" and give it a randomly 
       generated password.
        * Click Add.
        * Click Databases and then click New database.
        * For Name, enter the name of your database (for example, "polls"), and click Add.

Once you have a SQL host, configuring mysite/settings.py to point to your database. Change `your-database-name`, 
`your-database-user`, `your-database-host` , and `your-database-password` to match the settings created above. Note the 
instance name is not used in this configuration, and the host name is the IP address you created.


## Running locally

First make sure you have Django installed. It's recommended you do so in a 
[virtualenv](https://virtualenv.pypa.io/en/latest/). The requirements.txt
contains just the Django dependency.

    pip install -r requirements.txt

Once the database is setup, run the migrations.

    python manage.py migrate

If you'd like to use the admin console, create a superuser.

    python manage.py createsuperuser

The app can be run locally the same way as any other Django app. 

    python manage.py runserver

Now you can view the admin panel of your local site at

    http://localhost:8080/admin

# Deploying To Google Container Engine (Kubernetes)

## Build the polls container

Before the application can be deployed to Container Engine, you will need build and push the image to [Google Container Registry](https://cloud.google.com/container-registry/). 

    docker build -t gcr.io/your-project-id/polls .
    gcloud docker push gcr.io/your-project-id/polls

Alternatively, this can be done using 

    make push
    

## Deploy to the application

### Serve the static content

Collect all the static assets into the static/ folder.

    python manage.py collectstatic
    
When DEBUG is enabled, Django can serve the files directly from that folder. For production purposes, you should 
serve static assets from a CDN. Here are instructions for how to do this using Google Cloud Storage.

Upload it to CloudStorage using the `gsutil rsync` command

    gsutil rsync -R static/ gs://<your-gcs-bucket>/static 

Now your static content can be served from the following URL:

    http://storage.googleapis.com/<your-gcs-bucket/static/

Change the `STATIC_URL` in mysite/settings.py to reflect this new URL by uncommenting
the appropriate line and replacing `<your-cloud-bucket>`

### Create the Kubernetes resources

This application is represented in a single Kubernetes config, called `polls`. First, replace the 
GCLOUD_PROJECT in `polls.yaml` with your project ID. Alternatively, run `make template` with your
GCLOUD_PROJECT environment variable set.

    kubectl create -f polls.yaml
    
Alternatively this create set can be done using the Makefile
    
    make deploy

Once the resources are created, there should be 3 `polls` pods on the cluster. To see the pods and ensure that 
they are running:

    kubectl get pods

If the pods are not ready or if you see restarts, you can get the logs for a particular pod to figure out the issue:

    kubectl logs pod-id

Once the pods are ready, you can get the public IP address of the load balancer:

    kubectl get services polls

You can then browse to the public IP address in your browser to see the bookshelf application.

When you are ready to update the replication controller with a new image you built, the following command will do a 
rolling update

    kubectl rolling-update polls --image=gcr.io/${GCLOUD_PROJECT}/polls
    
which can also be done with the `make update` command.    


## Issues

Please use the Issue Tracker for any issues or questions.

## Contributing changes

* See [CONTRIBUTING.md](CONTRIBUTING.md)


## Licensing

* See [LICENSE](LICENSE)
