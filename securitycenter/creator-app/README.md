% SCC Tools: **Creator**
% Security Cloud Command Center Tools

\setcounter{section}{0}
\setcounter{secnumdepth}{10}
\newpage

# Introduction

_Estimated time to complete the installation: **30 minutes**_

This application is an example of how to **periodically run queries** against Security Command Center and then send the query results to a Google Cloud Pub/Sub topic.

This application is also an example of how to use the **filter**, **read time** and **compare duration** parameters of the Security Command Center API.

## Requirements \label{sec:requirements}

**_ATTENTION:_** Before we start, make sure you've gone through the section **'How to install the tools'** in the main  **`README-${version}.pdf`** file delivered in this package.
It contains **important pre-requisites and pre-installation instructions you must do** to proceed to the installation of this tool.

You will need to create a new Project and link an active _Google Cloud Billing Account_ to it to install **Creator**.
If you do not have the permissions to create Projects or Enable Billing, **you must look for help from someone in your Organization** who has the permissions to create Projects and enable Billing on that Project.

If you can create the **Creator** Project you will be the _Project Owner_ and have all the necessary permissions to run the installation, deploy and use the application.

If you can't create the Project, your administrator will need to give you the **Owner** or **Editor** Cloud IAM roles, or at least the following roles in your **Creator** Project:

* Viewer - `roles/viewer`
* Service Usage Admin - `roles/serviceusage.serviceUsageAdmin`
* API Keys Admin - `roles/serviceusage.apiKeysAdmin`
* Pub/Sub Admin - `roles/pubsub.admin`
* Cloud Datastore Owner - `roles/datastore.owner`
* Cloud Scheduler Admin - `roles/cloudscheduler.admin`
* App Engine Admin - `roles/appengine.appAdmin`
* Cloud Build Editor - `roles/cloudbuild.builds.editor`
* Service Account Admin - `roles/iam.serviceAccountAdmin`
* Service Account Key Admin - `roles/iam.serviceAccountKeyAdmin`
* Project IAM Admin - `roles/resourcemanager.projectIamAdmin`
* Storage Admin - `roles/storage.admin`
* Storage Object Admin - `roles/storage.objectAdmin`

_Note: If your user is not the **Project Owner** or don't have all of the required IAM roles, ask someone on your Organization to assign those roles to your user so you can continue with the installation process._

You will also need someone with Organization Administrator role to give the permissions listed below to the SCC Client Service Account (detailed in **section \ref{sec:scc_client_sa}**)

* Security Center Assets Viewer - `roles/securitycenter.assetsViewer`
* Security Center Findings Viewer - `roles/securitycenter.findingsViewer`

# Install the **Creator** application

## Step 1: Creating the Project

First, create the Project in which the **Creator** application will be installed. You can use the command below to accomplish this.

```bash
# the organization id where the project should be created
export organization_id=<your_org_id>

# project id to be created
export creator_project_id=<your_creator_project_id>

gcloud projects create ${creator_project_id} \
  --organization ${organization_id}
```

## Step 2: Linking the Project to a Billing Account

The Project in which **Creator** will be installed needs to have a linked _Billing Account_.

Usually you should ask your _Billing Administrator_ to link a valid Billing Account in your Project. However, if you have the permission to link Billing Accounts to a Project, you can use the commands below to accomplish this task.

_Note: If you want, you can learn more about 'Modifying a Project's Billing Settings' by following [this link](https://cloud.google.com/billing/docs/how-to/modify-project)._

```bash
# the project created to install the application
export creator_project_id=<your_creator_project_id>

# a valid billing Account ID to be linked to the
# project (ask your Billing Administrator which one to use)
# [Billing accounts](https://console.cloud.google.com/billing)
export billing=<your_billing_account_id>

gcloud beta billing projects link ${creator_project_id} \
  --billing-account ${billing}
```

_Note: If the above command fail, ask your _Billing Administrator_ for help._

## Step 3: Turning on Google App Engine

The **Creator** application uses Google App Engine(GAE) as its execution environment.
You need someone with the primitive role **Owner** to turn GAE on before installing the application.
If you are not an **Owner** of the **Creator** project **you must look for help from someone in your Organization** who has the **Owner** role on the **Creator** project to turn GAE on.

You can use the command below to turn GAE on:

```bash
# the project created to install the application
export creator_project_id=<your_creator_project_id>

# one region listed in
# [App Engine Regions](https://cloud.google.com/appengine/docs/locations)
export gae_region=<your-gae-region>

gcloud app create \
 --region  ${gae_region} \
 --project ${creator_project_id}
```

**Note:** _You **cannot change** an Google App Engine's region **after** you set it._

## Step 4: Enabling Google API's

The **Creator** application needs some Google APIs enabled in the Project.

Use the gcloud commands below to enable the necessary APIs:

```bash
# the project created to install the application
export creator_project_id=<your_creator_project_id>

gcloud services enable \
  securitycenter.googleapis.com \
  servicemanagement.googleapis.com \
  cloudresourcemanager.googleapis.com \
  appengine.googleapis.com \
  compute.googleapis.com \
  pubsub.googleapis.com \
  cloudbuild.googleapis.com \
  storage-component.googleapis.com \
  --project ${creator_project_id}
```

## Step 5: Create SCC Client Service Account \label{sec:scc_client_sa}

To create the SCC Client Service Account the user must have the following IAM roles:

* Organization Administrator - `roles/resourcemanager.organizationAdmin`
* Security Center Admin - `roles/securitycenter.admin`
* Service Account Admin -  `roles/iam.serviceAccountAdmin`
* Service Account Key Admin - `roles/iam.serviceAccountKeyAdmin`

_Note: If the user does not have these roles, ask for help from someone from your organization to execute the instructions in this section_

These roles are necessary to grant the following roles to the service account:

* Security Center Assets Viewer - `roles/securitycenter.assetsViewer`
* Security Center Findings Viewer - `roles/securitycenter.findingsViewer`

Create environment variables:

```bash
# set the organization id (to get your organization ID, please follow the link below)
# https://cloud.google.com/resource-manager/docs/creating-managing-organization
export organization_id=<your_organization_id>

# the project created to install the application
export creator_project_id=<your_creator_project_id>

# the project ID where the service account will be created
export scc_api_project_id=${creator_project_id}

# the working directory.
export working_dir=${HOME}/scc-tools-install

# enter in the installation working directory
cd ${working_dir}
```

Run these commands to create the service account:

```bash
# Create the Service Account
gcloud iam service-accounts create scc-viewer  \
 --display-name "SCC Viewer SA"  \
 --project ${scc_api_project_id}

# Download the service account key file
(cd setup; \
 gcloud iam service-accounts keys create \
 service_accounts/scc-viewer-${scc_api_project_id}-service-account.json \
 --iam-account scc-viewer@${scc_api_project_id}.iam.gserviceaccount.com)
```
You need an user with Organization Administrator role to give the organization level roles. If you are not an Organization Administrator
please contact someone on you organization with required permissions to execute below commands.

```bash
# Grant the Organization Level roles
gcloud beta organizations add-iam-policy-binding ${organization_id} \
 --member="serviceAccount:scc-viewer@${scc_api_project_id}.iam.gserviceaccount.com" \
 --role='roles/securitycenter.assetsViewer'
 
gcloud beta organizations add-iam-policy-binding ${organization_id} \
--member="serviceAccount:scc-viewer@${scc_api_project_id}.iam.gserviceaccount.com" \
--role='roles/securitycenter.findingsViewer'
```

If you already have that service account created and only need to download another key file, you can just run the following command:

_Note: If you are installing the SCC Tools in a new version of SCC API (e.g. from Alpha to Beta), do **not** use the same Service Account. You must create a new Service Account for the new version of the API._

```bash
(cd setup; \
export service_account_email=scc-viewer@${scc_api_project_id}.iam.gserviceaccount.com; \
export output_file=service_accounts/scc-viewer-${scc_api_project_id}-service-account.json; \
gcloud iam service-accounts keys create ${output_file} --iam-account=${service_account_email})
```

## Step 6: Creating the SCC API Key

The **Creator** application needs an API Key to call the SCC APIs. Follow these steps to create this key:

1. Go to `https://console.cloud.google.com/apis/credentials` in your **Creator** Project.
2. Click on `Create Credentials` and choose `API key`.
3. Copy the generated API key value. You will be asked for this value in the next sections.

## Step 7: Creating the publisher service account

The **Creator** application uses a service account to publish to topics.  
To create it and give  **Pub/Sub Publisher** role on the creator project run the commands below:

```bash
# the project created to install the application
export creator_project_id=<your_creator_project_id>

(cd setup; \
pipenv run python3 create_service_account.py \
  --name publisher \
  --project_id ${creator_project_id} \
  --roles_file roles/creator-pubsub.txt \
  --no-simulation)
```

To be able to send messages to a topic in another project you will need to give to the service account just created the **Pub/Sub Publisher** role on that project.

## Step 8: Deploy the **Creator** application

Open **Google Cloud Shell** and upload the following file to your `${HOME}` directory:

* scc-creator-${version}.zip

Set the environment variables required by the installation scripts.

**Note:** _You must set them with values that are valid in your context, editing the snippet below before running the commands._

```bash
# the scc tools release version you received.
export version=<release_version>

# directory to unzip the installation zip files.
export working_dir=${HOME}/scc-tools-install

# the organization id where these scripts will run
export organization_id=<your_org_id>

# the project created to install the application
export creator_project_id=<your_creator_project_id>

# absolute path to the Service Account file for the the Security Command Center API Project
export scc_sa_file=<absolute_path_to_scc_apiservice_account_file>

# SCC Api key to call the SCC APIs, created in previous section
export api_key=<your_scc_api_key>
```

Unzip the uploaded file and enter the working directory:

```bash
# unzip the uploaded files to a work directory
unzip -qo scc-creator-${version}.zip -d ${working_dir}

# enter the installation working directory
cd ${working_dir}
```

Now run the following command to create the remaining infrastructure, the Pub/Sub topics, and deploy the application:

**Note:** _If you want to just see a simulation of the execution of the following command (a dry run), use the option `--simulation`._

```bash
(cd setup; \
export publisher_sa_file=./service_accounts/${creator_project_id}_publisher.json; \
pipenv run python3 run_setup_creator.py \
  --organization_id ${organization_id} \
  --creator_project ${creator_project_id} \
  --creator_sa_file ${scc_sa_file} \
  --scc_api_key ${api_key} \
  --publisher_sa_file ${publisher_sa_file} \
  --no-simulation)
```

**Note:** _During the deployment, a token is created to validate the requests for the URLs in the APP used internally for the Google Pub/Sub integration, this value can be checked from the file .google_code_lab_creator_cloud_function_secret_client_key_demomode on your home directory._

# Using the **Creator** application

You can use the **Creator** application to periodically search for **Assets** or security **Findings** in the Security Command Center.

Before you can start using the **Creator** application you need to configure it.

## Configuring the **Creator** application

The **Creator** application has two configuration options: the **operation mode** and the **queries** to run.

### Operation modes

The application has two different operation modes:

* **DEMO** mode: when the application is on the **DEMO** mode, it **will not** run the queries periodically. For the query to be executed in **DEMO** mode you will need to post any message in a Pub/Sub topic created during the installation, `/project/${creator_project_id}/topic/demomode` , or use the helper script **load.py**.
* **PRODUCTION** mode: when the application is on the **PRODUCTION** mode, the configured queries **will be** triggered periodically by an App Engine Cron job.

In both cases the query results will be send to the a Pub/Sub topic.

You must be **Owner**, **Editor** or have the role **"Pub/Sub Admin"** or **"Pub/Sub Publisher"** on creator project to set the operation mode.

To manage both the **operation mode** and the **queries** you will use a helper script **load.py**.

Run the helper script to set the operation mode:

```bash
# Step 1: install Python dependencies:
(cd creator/cli; \
  pipenv --python 3.5.3; \
  pipenv install --ignore-pipfile)

# Step 2: set the application default login:
gcloud auth application-default login

# Step 3: Setting the mode
(cd creator/cli; \
pipenv run python3 load.py mode \
  --mode <PRODUCTION|DEMO> \
  --project ${creator_project_id})
```

**Note:** _We recommend first setting the application operation mode to **DEMO** mode for validation._

### Queries

You must be **Owner**, **Editor** or have the role **"Cloud Datastore Owner"** on creator project to upload and manage queries.

To upload a query the script needs the path to an YAML file that contains the query. There are some sample queries on the folder `creator/samples`. Lets use one of them for validation.

```bash
(cd creator/cli; \
pipenv run python3 load.py event_queries \
  --yaml_file ../samples/one_step_asset_for_testing.yaml \
  --project ${creator_project_id})
```

## Validating the installation

### Step 1: checking for the query you uploaded

```bash
(cd creator/cli; \
pipenv run python3 load.py list_queries \
  --project ${creator_project_id})
```

You should see a single query on the list with the name:  
**"find Assets of resourceType google.cloud.resourcemanager.Organization."**

### Step 2: Creating a test topic

```bash
gcloud pubsub topics create projects/${creator_project_id}/topics/testtopic \
  --project ${creator_project_id}
```

### Step 3: Creating a subscription

```bash
gcloud pubsub subscriptions create projects/${creator_project_id}/subscriptions/testsubscription \
  --topic testtopic \
  --topic-project ${creator_project_id} \
  --project ${creator_project_id}
```

### Step 4: Running the query

```bash
(cd creator/cli; \
pipenv run python3 load.py execute_queries \
  --project ${creator_project_id})
```

### Step 5: Pulling the results from the subscription

```bash
gcloud pubsub subscriptions pull projects/${creator_project_id}/subscriptions/testsubscription \
  --auto-ack \
  --limit 1 \
  --format json \
  --project ${creator_project_id}
```

The message is in the format shown on the section **'Appendix I - Notification Pub/Sub Topic message format'** in the main  **`README-${version}.pdf`** file delivered in this package.

## Managing Queries

You can also use the helper script to manage the queries. You can use the script to:

* Upload queries
* Execute all queries
* List all queries
* Delete a queries
* Delete all queries

### Uploading queries

```bash
(cd creator/cli; \
pipenv run python3 load.py event_queries \
  --yaml_file <path-to-query-file> \
  --project ${creator_project_id})
```

### Executing all queries

```bash
(cd creator/cli; \
pipenv run python3 load.py execute_queries \
  --project ${creator_project_id})
```

### Listing all queries

```bash
(cd creator/cli; \
pipenv run python3 load.py list_queries \
  --project ${creator_project_id})
```

### Deleting a queries

```bash
(cd creator/cli; \
pipenv run python3 load.py delete_query \
  --project ${creator_project_id} --key <key-to-be-deleted>)
```

The **key-to-be-deleted** value is the one read from the _list_queries_ results.

### Deleting all queries

```bash
(cd creator/cli; \
pipenv run python3 load.py delete_all_queries \
  --project ${creator_project_id})
```

## Query format

The **Creator App** uses the `list_assets` and `list_findings` APIs to retrieve information from Cloud SCC.
Both APIs only return items from a single organization.

The **Creator App** maps the available parameters passed to the API on the YAML files that contains the queries that are executed by the system.

Sample YAML file with a two-step query example:

```yaml
- name: "Find FORSETI findings on projects owned by dandrade"
  joins:
    - field: securityCenterProperties.resourceName
      kind: ASSET
      order: 1
      type: SINGLE
    - field: resourceName
      kind: FINDING
      order: 2
      type: MULTI
  steps:
    - duration: 43w
      kind: ASSET
      order: 1
      referenceTime:
        type: timestamp
        value: "2018-04-02T10:30:42+0400"
      where: "securityCenterProperties.resourceType = \"google.cloud.resourcemanager.Project\" AND securityCenterProperties.resourceOwners : \"dandrade\""
    - kind: FINDING
      order: 2
      referenceTime:
        type: from_now
        value: 1d+7h+20m
      where: "parent : \"organizations/000000000000/sources/0000000000000000000\""
  threshold:
    operator: gt
    value: 2
  topic: cloudflare_topic
```

**Note:** _On your environment you need to replace `organizations/000000000000/sources/0000000000000000000` with the actual value of the FORSETI security source id._

On this example we have a query "Find FORSETI findings on projects owned by dandrade" that has two steps: the first one that search projects owned by a user with login "dandrade" and the second one that search findings from FORSETI on projects found on the first step.

Let's review each field that is part of the example:

* **name**: It is an identifier in human readable form for the query
* **joins**: It is a list to explain which field from the result of the first step should be used to on the second step. Each element contains:
  * **order**: to identify if it is related to the first or second step
  * **kind**: to identify the entity it is related, currently one of ASSET or FINDING
  * **field**: from we are going to extract or construct the join information. Usually in queries with assets and findings it is the asset resourceName: _securityCenterProperties.resourceName_ on Assets and _resourceName_ on Findings .
  * **type**: that tell us if the field is a scalar value or an array. this is important because if you are extracting information from a **MULTI** field the system needs to split the array in individual values and if you are building the *where* for a step on a **MULTI** field the system needs to use the contains operator ":", instead of the equals operator "=".
* **steps**: a list with the actual information to be used when calling the asset or findings APIs. Each one contains:
  * **order**: field, to indicate if it is the first or the second step
  * **kind**: field to identify the entity it is related, currently one of ASSET or FINDING. They will be queried against the SCC API.
  * **where**: field with the actual query that will be sent to the API for this step. It can query securityCenterProperties, resourceProperties or Security Marks on [Assets](https://cloud.google.com/security-command-center/docs/reference/rest/v1beta1/organizations.assets/list#asset) and attributes, sourceProperties or Security Marks on [Findings](https://cloud.google.com/security-command-center/docs/reference/rest/v1beta1/organizations.sources.findings#Finding). You can use the contains operator ":", the equals operator "=" and the negation operator "-". You can also use AND and OR. It will be mapped to the `filter` field on the SCC API.
  * **fromLastJobExecution**: An optional field for FINDING steps that will automatically add a restriction to the **where** field value so that only findings created since the last execution of the query will satisfy the original **where** condition. It simulates the simultaneous use of  **referenceTime** and **duration** to set up an interval on the creation time for FINDING steps and will be removed when the **duration** query option becomes available for FINDING steps.
  * **referenceTime**: an optional field to represent the moment in time of the search. It will be mapped to the `read time` field on the SCC API. It has two modes:
    * **timestamp**: where you pass a fixed moment in time as a String in ISO 8601 format with time zone
    * **from_now**: where you inform a time interval to run before the current data and time.
      * The format is {#weeks}w+{#days}d+{#hours}h+{#minutes}m+{#seconds}s.
      * The reading time of the query will be the current date minus the time interval informed.
      * Examples: 4w would mean 4\*7\*24\*60\*60 seconds before the current date and 3d+15s would mean 3\*24\*60\*60  + 15 seconds before the current date time.
  * **duration**: an optional field, only valid for the ASSET kind representing a time amount in the form {#weeks}w+{#days}d+{#hours}h+{#minutes}m+{#seconds}s. it will represent an interval before the reference time when the asset existence will be validated. It will be mapped to the field `compare duration` on the SCC API.
  * **threshold**: an <operator,value> pair to set a condition on when the result of a query should trigger messages to be posted to a Pub/Sub Topic. This comparison is executed against the size of the response of the last step of the query. The Value must be a number and the Operator can be one of the following:
    * **lt** lower or equal
    * **le** lower than
    * **eq** equal
    * **ne** not equal
    * **ge** greater or equal
    * **gt** greater than
* The **topic** field,  an optional field with the name of a Pub/sub topic to where the results of this queries should be posted. If not present results will be posted to the default topic. if the topic does not exist it will be created by the application. It accepts the short format `topic_name` for topics on the **Creator** project or the full format  `/project/project_id/topic/topic_name` for topics in other projects.

**Important Note:** _If the size of the query does not satisfies the threshold condition **nothing will be posted to the Pub/Sub Topic**._

## Other query examples

### Working with datetime type query fields

#### How can we have a step that will help check if any firewall was created or deleted in a one-hour interval starting 5 minutes before the query execution?

```yaml
order: 1
kind: ASSET
where: "securityCenterProperties.resourceType = \"google.compute.Firewall\""
duration: "1h"
referenceTime:
  type: from_now
  value: "5m"
```

This could be used for example to periodically query the API.

#### How to create a step that will check if there was any network created or deleted in the first week of February?

```yaml
order: 1
kind: ASSET
where: "securityCenterProperties.resourceType = \"google.compute.Network\""
duration: "1w"
referenceTime:
  type: timestamp
  value: "2018-02-08T00:00:00+0400"
```

## Using Scalar and Multi-value fields

```yaml
order: 1
kind: ASSET
where: "securityCenterProperties.resourceType = \"google.cloud.resourcemanager.Project\""
```

**securityCenterProperties.resourceType** is an example of a scalar field and we can use both comparison operators, ':' and '='. The equality operator will do a full match and the ":" will do a substring match in the original value.

```yaml
order: 1
kind: ASSET
where: "securityCenterProperties.resourceOwners : \"dandrade\""
```

**securityCenterProperties.resourceOwners** is an example of a multi-value field.

A sample value could be

```yaml
securityCenterProperties.resourceOwners = ["useralpha@example.com","userbeta@example.com"]
```

on this case, to be able to query the field value for the user **useralpha** we could do:

```yaml
where: "securityCenterProperties.resourceOwners : \"useralpha@example.com\""
```

this is the available way to query a multi-value attribute for individual values. Currently the only multi-value attribute is the _securityCenterProperties.resourceOwners_ attribute.

## Changing the Cron Job interval

The initial Cron job interval is configured to _"every 15 minutes"_, meaning that every 15 minutes the job will trigger and call the **Creator** Application to run the current uploaded queries if the application is on _PRODUTION_ mode.

You can change the interval which the Cron job runs the queries following this guide
[Scheduling jobs with cron.yaml](https://cloud.google.com/appengine/docs/flexible/python/scheduling-jobs-with-cron-yaml) instructions.

The cron.yaml file is on folder `creator\appflex` and its original configuration is:

```yaml
cron:
- description: test task
  url: /events/processor
  schedule: every 15 minutes
```

After changing the cron.yaml, file run this gcloud command to upload the change:

```bash
(cd creator/appflex; \
gcloud app deploy cron.yaml)
```