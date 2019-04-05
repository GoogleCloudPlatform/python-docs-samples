# K8S cluster configuration

This how to assumes that you already have:

- a DNS project configured, beyond [original documentation](https://cloud.google.com/dns/quickstart), you can use [plan_dns.md](plan_dns.md) located in this folder to configure yours.
- a URL added on DNS project
- a project for install this project
- a CSCC project
- a Notification project already installed
- SSL certicates already generated, at the end of this document you can find a tool for it.
- you have a user with roles granted

## 1. Setup environment variables

```bash
export k8s_gcp_project_id=<project_id>
export organization_id=<organization_id>
export organization_display_name=<organization_display_name>
export scc_project_id=<scc_project_id>
export notification_topic=<notification_topic>
export notification_project_id=<notification_project>
```

## 2. Enable apis

```bash
gcloud services enable \
cloudapis.googleapis.com \
cloudbuild.googleapis.com \
clouddebugger.googleapis.com \
cloudtrace.googleapis.com \
compute.googleapis.com \
container.googleapis.com \
containerregistry.googleapis.com \
deploymentmanager.googleapis.com \
logging.googleapis.com \
monitoring.googleapis.com \
oslogin.googleapis.com \
replicapool.googleapis.com \
replicapoolupdater.googleapis.com \
resourceviews.googleapis.com \
servicemanagement.googleapis.com \
serviceusage.googleapis.com \
sourcerepo.googleapis.com \
sql-component.googleapis.com \
sqladmin.googleapis.com \
stackdriver.googleapis.com \
storage-api.googleapis.com \
storage-component.googleapis.com \
--project $k8s_gcp_project_id
```

## 3. SSL generation

### 3.1 Create ssl certificate

```bash
export query_builder_domain=<your_query_builder_domain>
export dns_zone=<your_dns_zone>
export dns_project_id=<your_dns_project_id>
export email=<your_email>

(cd setup;
pipenv run python3 ssl_generate.py \
--main_domain ${query_builder_domain} \
--dns_zone ${dns_zone} \
--dns_project_id ${dns_project_id} \
--email ${email} \
--no-simulation)
```

### 3.2 Extract generated certificates

```bash
export querybuilder_domain=<your_query_builder_domain>

echo querybuilder_domain=${querybuilder_domain}

(
cd setup;
unzip -q certs-${querybuilder_domain}.zip -d ~/ssl-certificates/
cp certs-${querybuilder_domain}.zip ~/ssl-certificates/;
)
```

## 4. IAM setup

### 4.1 SCC service account setup

#### 4.1.1 Create service account scc connection

```bash
gcloud iam service-accounts create scc-connection \
--project $scc_project_id
```

#### 4.1.2 Create service account key for scc connection

```bash
gcloud iam service-accounts keys create \
$scc_project_id-scc-connection.json \
--iam-account=scc-connection@$scc_project_id.iam.gserviceaccount.com
```

#### 4.1.3 Add roles to SCC service account

```bash
gcloud beta organizations add-iam-policy-binding $organization_id \
--member="serviceAccount:scc-connection@$scc_project_id.iam.gserviceaccount.com" \
--role='roles/securitycenter.editor'
```

### 4.2 SQL proxy service account setup

#### 4.2.1 Create service account for sql proxy

```bash
gcloud iam service-accounts create sql-proxy \
--project $k8s_gcp_project_id
```

#### 4.2.2 Create service account key for cloud sql connection

```bash
gcloud iam service-accounts keys create \
$k8s_gcp_project_id-sql-proxy.json \
--iam-account=sql-proxy@$k8s_gcp_project_id.iam.gserviceaccount.com
```

#### 4.2.3 Add roles for cloud sql service account

```bash
gcloud projects add-iam-policy-binding $k8s_gcp_project_id \
--member serviceAccount:sql-proxy@$k8s_gcp_project_id.iam.gserviceaccount.com \
--role roles/cloudsql.client
```

### 4.3 Notifier App service account setup

#### 4.3.1 Create service account for Notifier App

```bash
gcloud iam service-accounts create notifier-connection \
--project $notification_project_id
```

#### 4.3.2 Create service account key for Notifier App

```bash
gcloud iam service-accounts keys create \
$notification_project_id-scc-publish.json \
--iam-account=notifier-connection@$notification_project_id.iam.gserviceaccount.com
```

#### 4.3.3 Add roles to notifier app service account

```bash
gcloud projects add-iam-policy-binding $k8s_gcp_project_id \
--member="serviceAccount:notifier-connection@$notification_project_id.iam.gserviceaccount.com" \
--role='roles/pubsub.publisher'
```

### 4.4 Scheduler service account setup

#### 4.4.1 Create service account for Scheduler

```bash
gcloud iam service-accounts create scheduler-connection \
--project $k8s_gcp_project_id
```

#### 4.4.2 Create service account key for Scheduler

```bash
gcloud iam service-accounts keys create \
$k8s_gcp_project_id-qb-pubsub.json \
--iam-account=scheduler-connection@$k8s_gcp_project_id.iam.gserviceaccount.com
```

#### 4.4.3 Add roles to scheduler service account

```bash
gcloud projects add-iam-policy-binding $k8s_gcp_project_id \
--member="serviceAccount:scheduler-connection@$k8s_gcp_project_id.iam.gserviceaccount.com" \
--role='roles/pubsub.publisher'

gcloud projects add-iam-policy-binding $k8s_gcp_project_id \
--member="serviceAccount:scheduler-connection@$k8s_gcp_project_id.iam.gserviceaccount.com" \
--role='roles/pubsub.subscriber'
```

## 5. Cleanup default network

### 5.1 Delete firewall rules

```bash
gcloud compute firewall-rules list \
--project=$k8s_gcp_project_id \
--format='value(name)' | xargs -n1 -I{} \
gcloud compute firewall-rules \
delete {} \
--quiet \
--project=$k8s_gcp_project_id
```

### 5.2 Delete network default

```bash
gcloud compute networks delete default \
--quiet \
--project=$k8s_gcp_project_id
```

## 6. Setup network

### 6.1 Create network

```bash
gcloud compute networks create scc-tools-nw \
--subnet-mode=custom \
--project=$k8s_gcp_project_id
```

### 6.2 Create subnetwork

```bash
gcloud compute networks subnets create scc-tools-subnet \
--network=scc-tools-nw \
--region=us-central1 \
--range=10.1.0.0/19 \
--secondary-range=scc-tools-subnet-pods=10.2.0.0/19,scc-tools-subnet-services=10.3.0.0/22 \
--enable-private-ip-google-access \
--project=$k8s_gcp_project_id
```

### 6.3 Reserve a static IP address

```bash
gcloud compute addresses create querybuilder-web-static-ip --global --project "$k8s_gcp_project_id"
```

### 6.4 Create or update A record on dns to point to this IP

```bash
export EXTERNAL_IP=$(gcloud compute addresses list \
--filter="name=querybuilder-web-static-ip" \
--project "$k8s_gcp_project_id" \
--format "value(address)")

gcloud dns record-sets transaction start \
-z=${querybuilder_dns_zone} \
--project ${dns_project_id}

gcloud dns record-sets transaction add \
--zone ${querybuilder_dns_zone} \
--ttl 300 \
--name "${custom_domain}." \
--type A "${EXTERNAL_IP}"

gcloud dns record-sets transaction execute \
-z=${querybuilder_dns_zone} \
--project ${dns_project_id}
```

## 7. Setup cloud sql

### 7.1 Create cloud sql instance

```bash
gcloud sql instances create db-qb-instance \
--tier=db-n1-standard-2 \
--region=us-central1 \
--project=$k8s_gcp_project_id
```

### 7.2 Create cloud sql database

```bash
gcloud sql databases create query_builder \
--instance=db-qb-instance \
--charset=utf8 \
--project=$k8s_gcp_project_id
```

### 7.3 Get service account from cloud sql instance

```bash
export service_account_cloud_sql=$(gcloud sql instances describe db-qb-instance \
--project $k8s_gcp_project_id \
--format='value(serviceAccountEmailAddress)')
```

### 7.4 Create db bucket

```bash
gsutil mb \
-c regional \
-l us-central1 \
-p $k8s_gcp_project_id \
gs://${k8s_gcp_project_id}_db_load
```

### 7.5 Add the service account to the bucket ACL as a writer

```bash
gsutil acl ch \
-u $service_account_cloud_sql:W \
gs://${k8s_gcp_project_id}_db_load
```

### 7.6 Upload file to db bucket

```bash
gsutil cp \
scc-query-builder/k8s/db/dump-query_builder-201812281118.sql \
gs://${k8s_gcp_project_id}_db_load/
```

### 7.7 Add the service account to the import file as a reader

```bash
gsutil acl ch \
-u $service_account_cloud_sql:R \
gs://${k8s_gcp_project_id}_db_load/dump-query_builder-201812281118.sql
```

### 7.8 Load db structure

```bash
gcloud sql import sql db-qb-instance \
gs://${k8s_gcp_project_id}_db_load/dump-query_builder-201812281118.sql \
--database=query_builder \
--quiet \
--project $k8s_gcp_project_id
```

### 7.9 Remove acl given for cloud sql service account

```bash
gsutil acl ch -d $service_account_cloud_sql \
gs://${k8s_gcp_project_id}_db_load/dump-query_builder-201812281118.sql

gsutil acl ch -d $service_account_cloud_sql \
gs://${k8s_gcp_project_id}_db_load
```

### 7.10 Create a database user using the following command

```bash
gcloud sql users create proxyuser cloudsqlproxy~% \
--instance=db-qb-instance \
--password=[PASSWORD] \
--project=$k8s_gcp_project_id
```

### 7.11 Discover connection name

```bash
gcloud sql instances describe db-qb-instance --project=$k8s_gcp_project_id --format='value(connectionName)'
```

## 8. Setup Kubernetes

### 8.1 Create cluster

```bash

export expected_cluster_version=1.10
export cluster_version=$(gcloud container get-server-config --project=$k8s_gcp_project_id --quiet --zone=us-central1-a --format='value(validMasterVersions)' | tr ';' \\n | grep $expected_cluster_version)

gcloud beta container \
clusters create "scc-tools-gke-cluster" \
--zone "us-central1-a" \
--cluster-version "${cluster_version}" \
--username "admin" \
--machine-type "n1-highcpu-8" \
--image-type "COS" \
--disk-type "pd-ssd" \
--disk-size "100" \
--scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" \
--enable-autoscaling \
--min-nodes=1 \
--max-nodes=5 \
--network "scc-tools-nw" \
--subnetwork "scc-tools-subnet" \
--cluster-ipv4-cidr=10.56.0.0/13 \
--addons HorizontalPodAutoscaling,HttpLoadBalancing \
--enable-stackdriver-kubernetes \
--enable-autoupgrade \
--enable-autorepair \
--project "$k8s_gcp_project_id"
```

### 8.2 Setup kubectl to add context from GKE cluster

```bash
gcloud container clusters get-credentials \
scc-tools-gke-cluster \
--zone us-central1-a \
--project "$k8s_gcp_project_id"
```

### 8.3 Load certificates as secret

```bash
export prefix_sub_domains=prod
export custom_domain=${prefix_sub_domains}.${querybuilder_domain}

export ssl_key=~/ssl-certificates/certs/${custom_domain}/privkey1.pem
export ssl_cert=~/ssl-certificates/certs/${custom_domain}/cert1.pem

kubectl create secret tls querybuilder-ssl-secret \
--key $ssl_key \
--cert $ssl_cert
```

### 8.4 Add the service account to connect to scc as a secret env

```bash
kubectl create secret generic scc-account \
--from-file=scc-credentials=$scc_project_id-scc-connection.json
```

### 8.5 Add the service account to connect to db as a secret file

```bash
kubectl create secret generic cloudsql-instance-credentials \
--from-file=credentials.json=$k8s_gcp_project_id-sql-proxy.json
```

### 8.6 Add user and password to connect to instance as a secrect

```bash
kubectl create secret generic cloudsql-db-credentials \
--from-literal=username=proxyuser \
--from-literal=password=[PASSWORD]
```

### 8.7 Add general configurations as a configmap

```bash
kubectl create configmap general-config \
--from-literal=organization_id=${organization_id} \
--from-literal=organization_display_name=${organization_display_name}
```

### 8.8 Add notifier variables as configmap

```bash
kubectl create configmap notification-config \
--from-literal=organization_id="${organization_id}" \
--from-literal=notification_topic="${notification_topic}"
```

### 8.9 Add scheduler variables as configmap

```bash

export scheduler_topic_name="projects/${k8s_gcp_project_id}/topics/qb-scheduler"
export scheduler_subscriptions_name="projects/${k8s_gcp_project_id}/subscriptions/qb-scheduler-subscription"

kubectl create configmap scheduler-config \
--from-literal=topic.name="${scheduler_topic_name}" \
--from-literal=subscriptions.name="${scheduler_subscriptions_name}"
```

### 8.10 Add clean up variables as configmap

```bash
export cleanup_topic_name="projects/${k8s_gcp_project_id}/topics/qb-cleanup"
export cleanup_subscriptions_name="projects/${k8s_gcp_project_id}/subscriptions/qb-cleanup-subscription"

kubectl create configmap cleanup-config \
--from-literal=topic.name="${cleanup_topic_name}" \
--from-literal=subscriptions.name="${cleanup_subscriptions_name}"
```

### 8.11 Add the service account to connect to topic on querybuilder and on notifier project as a secret env

```bash
kubectl create secret generic scc-scheduler \
--from-file=pubsub.credentials=$k8s_gcp_project_id-qb-pubsub.json \
--from-file=notifier.credentials=$notification_project_id-scc-publish.json
```

## 9. Setup container builder

### 9.1 Create repository

```bash
gcloud source repos create scc-tools --project $k8s_gcp_project_id
```

### 9.2 Adding the repository as a remote

[Guide for adding a repository as a remote](https://cloud.google.com/source-repositories/docs/adding-repositories-as-remotes)

```bash
export k8s_environment_name=prod
git config --global credential.'https://source.developers.google.com'.helper gcloud.sh

git remote add google-$k8s_environment_name \
https://source.developers.google.com/p/$k8s_gcp_project_id/r/scc-tools
```

### 9.3 Setup container build trigger

#### 9.3.1 Open page

```bash
echo 'Setup container build trigger step 1: Open the url below on a window'

echo https://console.cloud.google.com/gcr/triggers?organizationId=$organization_id&project=$k8s_gcp_project_id
```

### 9.4 Grant role to CloudBuild service account

```bash
export k8s_gcp_project_id=<project_id>;
export project_number=$(gcloud projects list --filter="projectId:$k8s_gcp_project_id" --format='value(project_number)')
gcloud projects add-iam-policy-binding $k8s_gcp_project_id  --member=serviceAccount:$project_number@cloudbuild.gserviceaccount.com --role=roles/container.developer
```

### 9.5 Push code to repository

```bash
export k8s_environment_name=prod
export local_branch=develop
export remote_branch=develop
git push google-$k8s_environment_name $local_branch:$remote_branch
```

### 9.6 Fill page on build trigger

Setup container build trigger step 2: Fill the trigger

Name : ""

Trigger type : branch

Branch regex: develop

Build configuration: cloudbuild.yaml

Click: Save

## 10. Setup application on Kubernetes

### 10.1 Deploy real application

```bash
(
cd scc-query-builder;
export k8s_environment_name=prod
kubectl apply -f k8s/${k8s_environment_name}
)
```

### 10.2 Verify deployment

```bash
export prefix_sub_domains=prod
export dashless_domain="<your_domain>"
export querybuilder_domain="querybuilder.${dashless_domain}"
export custom_domain=${prefix_sub_domains}.${querybuilder_domain}
export querybuilder_url="https://${custom_domain}"
watch curl -s $querybuilder_url
```

### 10.3 Setup oauth consent

### 10.4 Setup credentials

Authorized redirect URIs needs to include:

```bash
echo $querybuilder_url
echo $querybuilder_url/_gcp_gatekeeper/authenticate
```

### 10.5 Define oauth variables

```bash
export oauth_client_id=[get it from ui]
export oauth_client_secret=[get it from ui]
```

### 10.6 Turn on IAP

#### 10.6.1 Turn on IAP for frontend

```bash
export frontend_backend_service=$(gcloud compute backend-services list --project $k8s_gcp_project_id --format='value(name)' --filter='description~frontend')

gcloud compute backend-services update $frontend_backend_service \
--global \
--iap=enabled,oauth2-client-id=$oauth_client_id,oauth2-client-secret=${oauth_client_secret} \
--project $k8s_gcp_project_id
```

#### 10.6.2 Turn on IAP for load balance

```bash
export load_balance_backend_service=$(gcloud compute backend-services list --project $k8s_gcp_project_id --format='value(name)' --filter='description~default-http-backend')

gcloud compute backend-services update $load_balance_backend_service \
--global \
--iap=enabled,oauth2-client-id=$oauth_client_id,oauth2-client-secret=${oauth_client_secret} \
--project $k8s_gcp_project_id
```

#### 10.6.3 Add Audience to validate IAP header as configmap

```bash
export frontend_backend_service_id=$(gcloud compute backend-services list --project $k8s_gcp_project_id --format='value(id)' --filter='description~frontend')

export project_number=$(gcloud projects describe $k8s_gcp_project_id --format='value(projectNumber)')

kubectl create configmap iap-config \
--from-literal=iap.audience=/projects/$project_number/global/backendServices/$frontend_backend_service_id
```

Authorized redirect URIs needs to include:

```bash
echo $querybuilder_url
echo $querybuilder_url/_gcp_gatekeeper/authenticate
```

## 11. Add topics and subscription for Scheduler and Clean Up

### 11.1 Add topic and subscription for Scheduler

```bash
gcloud pubsub topics create qb-scheduler --project $k8s_gcp_project_id
gcloud pubsub subscriptions create qb-scheduler-subscription --topic qb-scheduler  --project $k8s_gcp_project_id
```

### 11.2 Verify the association with Notifier App Push subscription given topic

```bash
gcloud pubsub subscriptions list
```

### 11.3 Add topic and subscription for Clean up

```bash
gcloud pubsub topics create qb-cleanup --project $k8s_gcp_project_id
gcloud pubsub subscriptions create qb-cleanup-subscription --topic qb-cleanup --project $k8s_gcp_project_id
```

### 11.4 Verify the association with clean up subscription given topic

```bash
gcloud pubsub subscriptions list  --project $k8s_gcp_project_id
```

## 12. Cleanup

```bash
gcloud beta container \
    clusters delete "scc-tools-gke-cluster" \
    --project "$k8s_gcp_project_id"
```

## 13. Troubleshooting

### 13.1 Get logs from your containers

You will need your backend Pod name, for this you can execute the following command:

```bash
kubectl get pods
```

Then you will be able to get your logs, you will pass your Pod name, and your container name. In this case, is the Cloud SQL container.

```bash
kubectl logs backend-b8c64685f-jn5lj cloudsql-proxy
```