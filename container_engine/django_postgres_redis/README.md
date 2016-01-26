This project is owned by Google copyright 2016 but is not an official Google-product nor officially maintained or 
supported by Google.

# Getting started with Django on Google Container Engine (Kubernetes)

Since this project demonstrates deploying Postgres and Redis to the cluster, it's slightly involved. For a simpler
example of Django on Container Engine/Kubernetes, try 

    github.org/GoogleCloudPlatform/python-docs-samples/container_engine/django_tutorial
 
 which also deploys Django to  Kubernetes but uses a CloudSQL managed MySQL database, no cache, no 
secrets, and does not demonstrate autoscaling.

This repository is an example of how to run a [Django](https://www.djangoproject.com/) 
app on Google Container Engine. It was created to go with a slide deck created here.

https://speakerdeck.com/waprin/deploying-django-on-kubernetes

This project walks through setting up this project on a Google Container Engine Kubernetes cluster. These 
instructions should work on other Kubernetes platforms with some adjustments. should also deploy
 on other Kubernetes providers besides Google Container. Specifically, cluster creation steps, disks, load balancers, 
, cloud storage options, and node autoscalers should get replaced by their equivalents on your platform. 
 
This project demonstrates how to create a PostgreSQL database and Redis cache within your cluster. It also contains
 an image to simulate load on your cluster to demonstrate autoscaling. The app is inspired by the 
[PHP-Redis Guestbook example](https://github.com/kubernetes/kubernetes/tree/master/examples/guestbook/php-redis).

Please submit any code or doc issues to the issue tracker!

## Makefile

Several commands listed below are provided in simpler form via the Makefile. Many of them use the GCLOUD_PROJECT 
environment variable, which will be picked up from your gcloud config. Make sure you set this to the correct project,

    gcloud config set project <your-project-id>
    
There are more Makefiles in sub-directories to help build and push specific images.

## Pre-requisites

1. Install [Docker](https://www.docker.com/).
 
1. Create a project in the [Google Cloud Platform Console](https://console.cloud.google.com).

1. [Enable billing](https://console.cloud.google.com/project/_/settings) for your project.

1. [Enable APIs](https://console.cloud.google.com/flows/enableapi?apiid=datastore,pubsub,storage_api,logging,plus) 
for your project. The provided link will enable all necessary APIs, but if you wish to do so manually you will need Datastore, Pub/Sub, Storage, and Logging.

1. Install the [Google Cloud SDK](https://cloud.google.com/sdk)

        $ curl https://sdk.cloud.google.com | bash 
        $ gcloud init

1. Create a cluster for the bookshelf application:

    `gcloud container clusters create guestbook \
        --scope "https://www.googleapis.com/auth/userinfo.email","cloud-platform" \
        --num-nodes 2
    gcloud container clusters get-credentials guestbook`
    
The get-credentials commands initializes the kubectl CLI tool with the cluster you just created.    

Alternatively, you can use the Makefile:
    
    make create-cluster

### A note about cost

The --num-nodes flag in the cluster create specifies how many instances are created. Container Engine orchestrator is 
free up to 5 instances, but you will pay for the instances themselves, so to minimize costs just create 1 node.
 
 At the end of the tutorial, run 
 
    gcloud container clusters delete guestbook
    gcloud compute disks delete pg-data
    
or

    make delete
    
To delete the cluster and not get charged for continued use. Deleting resources you are not using is especially 
important if you run the autoscaling example to create many instances.
  

## Running PostgreSQL and Redis

The Django app depends on a PostgreSQL and Redis service. While this README explains how to deploy those services within
the Kubernetes cluster, for local purposes you may want to run them locally or elsewhere. Looking in mysite/settings.py,
you can see the app looks for several environment variables. 


The first environment variable `NODB`, if set to 1, uses
a SQLite database and an in-memory cache, allowing the app to run without connecting to a real database. This is useful
 to test the app locally without Postgres/Redis, or deploy it to Kubernetes without Postgres/Redis. Instead, it will
 use a local SQLite file and in-memory cache. In the Kubernetes cluster, each container will have its own SQLite 
 database and memory-cache, so the persistence and cache storage of the values will not be shared between containers 
 so will not be right. The NODB setting is just to help debug incrementally and should be turned off.

Once NODB is disabled, you can connect to an external PostgreSQL or Redis service, or read further to learn how to 
setup these services within the cluster. Once you have host values for these services, you can set 
POSTGRES_SERVICE_HOST, REDIS_MASTER_SERVICE_HOST, and REDIS_SLAVE_SERIVCE_HOST with their appropriate values when 
runnig locally. When running on Kubernetes these variables will be automatically populated. See 
guestbook/mysite/settings.py for more detail.


If you want to emulate the Kubernetes environment locally, you can use env.template as a starting point for a file that 
can export these environment variables locally. Once it's created, you can source it to add them to your local 
enviornment:

# create .env file from env.template example
# source .env

Don't check the file with your environment variable values into version control.

## Running locally

First make sure you have Django installed. It's recommended you do so in a 
[virtualenv](https://virtualenv.pypa.io/en/latest/). The requirements.txt
contains just the Django dependency.

    pip install -r requirements.txt

The app can be run locally the same way as any other Django app. 

    # disable Postgres and Redis until we set them up
    cd guestbook
    export NODB=1
    python manage.py runserver

# Deploying To Google Container Engine (Kubernetes)

## Build the Guestbook container

Within the Dockerfile, NODB is turned on or off. Once you have deployed PostgreSQL or Redis, you can disable this 
flag. If you deploy those services within Kubernetes, the environment variables will be automatically populated. 
Otherwise you should set the environment variables manually using ENV in the Dockerfile.

Before the application can be deployed to Container Engine, you will need build and push the image to [Google Container Registry](https://cloud.google.com/container-registry/). 

    cd guestbook
    # Make sure NODB is enabled and set to 1 in the Dockerfile if you still haven't setup Postgres and REDIS
    docker build -t gcr.io/your-project-id/guestbook .
    gcloud docker push gcr.io/your-project-id/guestbook

Alternatively, this can be done using 

    make push
    
## Deploy to the application

## Deploying the frontend to Kubernetes

The Django application is represented  in Kubernetes config, called `frontend`. First, replace the 
GCLOUD_PROJECT in `kubernetes_config/frontend.yaml` with your project ID. Alternatively, run `make template`, which 
should automatically populate the GCLOUD_PROJECT environment variable with your `gcloud config` settings, and replace
$GCLOUD_PROJECT in the kubernets config tmplates with your actual project name.



Once you've finished following the above instructions on how to build your container, it needs to be 
pushed to a Docker image registry that Kubernetes can pull from. One option is Docker hub, but in these examples we use
 Google Container Registry. 

    cd guestbook
    make build
    make push

Once the image is built, it can be deployed in a Kubernetes pod. kubernetes_config/frontend.yalm contains the 
Replication Controller to spin up Pods with this image, as well as a Service with an external load balancer. However,
the frontend depends on secret passwords for the database, so before it's deployed, a Kubernetes Secret resource with
 your database passwords must be created.
 
### Create Secrets

 Even if NODB is enabled, the frontend replication controller is configured to use the Secret volume, so it must
 be created in your cluster first.
 
 Kubernetes [Secrets](http://kubernetes.io/v1.1/docs/user-guide/secrets.html) are used to store the database password.
 They must be base64 encoded and store in `kubernetes/configs/db.password.yaml`. A template containing an example config
 is created, but your actual Secrets shoudl not be added to source control. 
 
 In order to get the base64 encoded password, use the base64 tool
 
     echo mysecretpassword | base64 
     
 Then copy and paste that value into the appropriate part of the Secret config (your-base64-encoded-pw-here)
 
     kubectl create -f kubernetes_configs/db_password.yaml
 
 In the Postgres and Frontend replication controller, these Secrets are mounted onto their pods. In their Dockerfile,
 they are read into environment variables.
 
### Create the frontend Service and Replication Controller
 
    kubectl create -f kubernetes_config/frontend.yaml
    
Alternatively this create set can be done using the Makefile
    
    make deploy

Once the resources are created, there should be 3 `frontend` pods on the cluster. To see the pods and ensure that 
they are running:

    kubectl get pods
    
To get more information about a pod, or dig into why it's having problem starting, try
  
    kubectl describe pod <pod-id>

If the pods are not ready or if you see restarts, you can get the logs for a particular pod to figure out the issue:

    kubectl logs <pod-id>

Once the pods are ready, you can get the public IP address of the load balancer:

    kubectl get services frontend

You can then browse to the external IP address in your browser to see the bookshelf application.

When you are ready to update the replication controller with a new image you built, the following command will do a 
rolling update

    kubectl rolling-update frontend --image=gcr.io/${GCLOUD_PROJECT}/frontend
    
which can also be done with the `make update` command.    

## Create the Redis cluster

Since the Redis cluster has no volumes or secrets, it's pretty easy to setup:

    kubectl create -f kubernetes_config/redis_cluster.yaml

This creates a redis-master read/write service and redis-slave service. The images used are configured to properly 
replicate from the master to the slaves.

There should only be one redis-master pod, so the replicatoin controller configures 1 replicas. There can be many
redis-slave pods, so if you want more you can do:

    kubectl scale rc redis-slave --replicas=5

## Create PostgreSQL

PostgresSQL will need a disk backed by a Volume to run in Kubernetes. For this example, we create a persistent disk
using a GCE persistent disk:

    gcloud compute disks create pg-data  --size 500GB

or
    make disk

Edit `kubernetes_config/postgres.yaml` volume name to match the name of the disk you just created, if different.

For Postgres, the secrets need to get populated and a script to initialize the database needs to be added, so a image
should be built:
 
    cd postgres_image
    make build
    make push
    
Finally, you should be able to create the PostgreSQL service and pod.

    kubectl create -f kubernetes_config/postgres.yaml
    
Only one pod can read and write to a GCE disk, so the PostgreSQL replicaiton controller is set to control 1 pod. 
Don't scale more instances of the Postgres POD. 
    
### Re-Deploy The Frontend and Run Migrations

Now that the database and redis service are created, you should rebuild the frontend guestbook image with NODB
disabled.

    cd guestbook
    # edit Dockerfile to comment out NODB
    make build
    make push

With this new image, the replication controller should be updated. One way is to do a rolling update

    make update
    
This will safely spin down the old images and replace it with the new image. However, for development purposes
it can be quicker to scale the controller to 0 and then back up.
 
     kubectl scale scale rf frontend --replicas=0
     kubectl scale scale rf frontend --replicas=3

Finally, the Django migrations must be run to create the table. This can also be accomplished with kubectl-exec, this
time with the frontend pod. However, make sure your frontend-pod is actually talking to the database. If you earlier
built the image with NODB, rebuild it with NODB commented out. Then you can run the migrations:

	kubectl exec $(FRONTEND_POD_NAME) -- python /app/manage.py migrate
	
replacing FRONTEND_POD_NAME with the appropriate name, or automatically:
 	
    make migrations

### Serve the static content

When DEBUG is enabled, Django can serve the files directly from that folder. Currently, the app is configured
 to serve static content from the files that way to simplify development. For production purposes, you should disable
  the DEBUG flag and serve static assets from a CDN. 

The application uses [Google Cloud Storage](https://cloud.google.com/storage) to store static content. You can 
alternatively use a CDN of your choice. Create a bucket for your project:

    gsutil mb gs://<your-project-id>
    gsutil defacl set public-read gs://<your-project-id>
    
or 

    make create-bucket

Collect all the static assets into the static/ folder.

    python manage.py collectstatic

Upload it to CloudStorage using the `gsutil rsync` command

    gsutil rsync -R static/ gs://<your-gcs-bucket>/static 

Now your static content can be served from the following URL:

    http://storage.googleapis.com/<your-gcs-bucket/static/

Change the `STATIC_URL` in mysite/settings.py to reflect this new URL by uncommenting
the appropriate line and replacing `<your-cloud-bucket>`


### Load Testing and Autoscaling (beta feature)

Please note that autoscaling is a beta feature.

load_test_image provides a super minimal load generator - it hits a CPU intensive endpoint in a loop with curl. First
build the image:

    cd load_testing_image
    make build
    make push

Then create the Replication Controller and scale some clients: 
  
    kubectl create -f kubernetes_config/load_tester.yaml
    kubectl scale rc load --replicas=20
  
to generate load. Then

    make autoscaling
  
will create both Node autoscaling (gcloud) and Pod autoscaling (Kubernetes Horizontal Pod Autoscaling).

Again, by default this will scale to 10 nodes whcih you will be charged for, so pleaes disable autoscaling and scale 
the nodes back down or delete the cluster if you don't want to pay for sustained use of the 10 instances.

For more sophisticated load testing with Kubernetes, see:

https://cloud.google.com/solutions/distributed-load-testing-using-kubernetes

## Issues

Please use the Issue Tracker for any issues or questions.

## Contributing changes

* See [CONTRIBUTING.md](CONTRIBUTING.md)


## Licensing

* See [LICENSE](LICENSE)
