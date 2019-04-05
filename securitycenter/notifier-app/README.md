% SCC Tools: **Notifier**
% Security Cloud Command Center Tools

\setcounter{section}{0}
\setcounter{secnumdepth}{10}
\newpage

# Introduction

_Estimated time to complete the installation: **30 minutes**_

The **Notifier** Application is an example of how read and process the messages created by the **Creator** Application and send the Assets and Findings to multiple notification channels like email, SMS or Jira.

## Requirements \label{sec:requirements}

**_ATTENTION:_** Before we start, make sure you've gone through the section **'How to install the tools'** in the main  **`README-${version}.pdf`** file delivered in this package.
It contains **important pre-requisites and pre-installation instructions you must do** to proceed to the installation of this tool.

If you are going to use `SendGrid` if will need at least a [trial account](https://sendgrid.com/free/) to have an API KEY and an email to use as the sender

If you are going to use `Twilio` to send SMS messages you will need at least a [trial account](https://www.twilio.com/try-twilio) to get an account sid, and AUTH token and a Twilio number.

If you are going to use `JIRA` you will need at least a [account](https://www.atlassian.com/software/jira/try) with a project create an at least one use which will be the one the issue will assigned to.

You will need to create a new Project and link an active _Google Cloud Billing Account_ to it to install **Notifier**.
If you do not have the permissions to create Projects or Enable Billing, **you must look for help from someone in your Organization** who has the permissions to create Projects and enable Billing on that Project.

If you can create the **Notifier** Project you will be the _Project Owner_ and have all the necessary permissions to run the installation, deploy and use the application.

If you can't create the Project, your administrator will need to give you the **Owner** or **Editor** Cloud IAM roles, or at least the following roles in your **Notifier** Project:

* Viewer - `roles/viewer`
* Service Usage Admin - `roles/serviceusage.serviceUsageAdmin`
* API Keys Admin - `roles/serviceusage.apiKeysAdmin`
* Compute Storage Admin - `roles/storage.admin`
* Storage Admin - `roles/storage.admin`
* Storage Object Admin - `roles/storage.objectAdmin`
* Pub/Sub Admin - `roles/pubsub.admin`
* Cloud Functions Developer - `roles/cloudfunctions.developer`
* Service Account User - `roles/iam.serviceAccountUser`
* Service Management Administrator - `roles/servicemanagement.admin`
* Cloud Scheduler Admin - `roles/cloudscheduler.admin`
* App Engine Admin - `roles/appengine.appAdmin`
* Cloud Tasks Queue Admin - `roles/cloudtasks.queueAdmin`

_Note: If your user is not the **Project Owner** or don't have all of the required IAM roles, ask someone on your Organization to assign those roles to your user so you can continue with the installation process._

# Install the **Notifier** application

## Step 1: Create the Project

Create the Project in which the **Notifier** application will be installed. You can use the command below to accomplish this.

```bash
# the organization id where the project should be created
export organization_id=<your_org_id>

# project id to be created
export notifier_project_id=<your_notifier_project_id>

gcloud projects create ${notifier_project_id} \
  --organization ${organization_id}
```

## Step 2: Link the Project to a Billing Account

The Project in which **Notifier** will be installed needs to have a linked _Billing Account_.

Usually you should ask your _Billing Administrator_ to link a valid Billing Account in your Project. However, if you have the permission to link Billing Accounts to a Project, you can use the commands below to accomplish this task.

_Note: If you want, you can learn more about 'Modifying a Project's Billing Settings' by following [this link](https://cloud.google.com/billing/docs/how-to/modify-project)._

```bash
# the project created to install the application
export notifier_project_id=<your_notifier_project_id>

# a valid billing Account ID to be linked to the
# project (ask your Billing Administrator which one to use)
# [Billing accounts](https://console.cloud.google.com/billing)
export billing=<your_billing_account_id>

gcloud beta billing projects link ${notifier_project_id} \
  --billing-account ${billing}
```

_Note: If the above command fail, ask your _Billing Administrator_ for help._

## Step 3: Turn on Google App Engine

The **Notifier** application uses Google App Engine(GAE) as its execution environment.
You need someone with the primitive role **Owner** to turn GAE on before installing the application.
If you are not an **Owner** of the **Notifier** project **you must look for help from someone in your Organization** who has the **Owner** role on the **Notifier** project to turn GAE on.

You can use the command below to turn GAE on:

```bash
# the project created to install the application
export notifier_project_id=<your_notifier_project_id>

# one region listed in
# [App Engine Regions](https://cloud.google.com/appengine/docs/locations)
export gae_region=<your-gae-region>

gcloud app create \
 --region  ${gae_region} \
 --project ${notifier_project_id}
```

**Note:** _You **cannot change** an Google App Engine's region **after** you set it._

## Step 4: Enable API's

The **Notifier** application needs some Google APIs enabled in the Project.

Use the gcloud commands below to enable the necessary APIs:

```bash
# the project created to install the application
export notifier_project_id=<your_notifier_project_id>

gcloud services enable \
  securitycenter.googleapis.com \
  servicemanagement.googleapis.com \
  appengine.googleapis.com \
  cloudresourcemanager.googleapis.com \
  cloudfunctions.googleapis.com \
  --project ${notifier_project_id}
```

## Step 5: Deploy the **Notifier** application

Open **Google Cloud Shell** and upload the following file to your `${HOME}` directory:

* scc-notifier-${version}.zip

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
export notifier_project_id=<your_notifier_project_id>

# the service name prefix for the Google Cloud endpoint. Fixed value "notifier"
export notifier_project_endpoint=notifier

# one region listed in
# [Cloud Functions Locations](https://cloud.google.com/functions/docs/locations)
export region=<your_region>

# a bucket that is used on the cloud function deploy
# [Google storage bucket](https://cloud.google.com/storage/)
export notifier_cf_bucket=<your_cloud_function_bucket>
```

Unzip the uploaded file and enter the working directory:

```bash
# unzip the uploaded files to a work directory
unzip -qo scc-notifier-${version}.zip -d ${working_dir}

# enter the installation working directory
cd ${working_dir}
```

Now run the following command to create the remaining infrastructure and deploy the application:

**Note:** _If you want to just see a simulation of the execution of the following command (a dry run), use the option `--simulation`._

```bash
(cd setup; \
pipenv run python3 run_setup_notifier.py \
  --organization_id ${organization_id} \
  --region ${region} \
  --notifier_bucket ${notifier_cf_bucket} \
  --notifier_appengine_version ${notifier_project_endpoint} \
  --notifier_project ${notifier_project_id} \
  --no-simulation)
```

# Using the **Notifier** application

You can use the **Notifier** application to sent notifications to configured users for **Assets** or security **Findings** that where publish to a Pub/Sub topic by the **Creator** Application.

Before you can start using the **Notifier** application you need to configure it.

## Configuring the **Notifier** application

On **Notifier** you can turn on/off the processing of messages, set and configure the active notification channels, set rules to tell which messages will be processed and add extra info to the message. Every time you change those configuration you should stop the **Notifier** application of processing messages.

You will need the **"Service Management Administrator"** role to be able to configure the **Notifier** application.

You will need to create an access token and build the URL you will need to use to call the endpoint service.

### Step 1: Creating an access token

```bash
gcloud auth application-default login

export NOTIFIER_ACCESS_TOKEN=$(gcloud beta auth application-default print-access-token)
```

### Step 2: Getting the API endpoint

```bash
export NOTIFIER_API_ENDPOINT_URL=$(gcloud app services browse api-service \
--no-launch-browser \
--format="value(url)" \
--project ${notifier_project_id})
export NOTIFIER_API_ENDPOINT_URL=$NOTIFIER_API_ENDPOINT_URL/_ah/api
```

### Step 3: Stop processing messages

```bash
(cd notifier/tools; \
pipenv --python 3.5.3 ; \
pipenv install --ignore-pipfile)

(cd notifier/tools; \
pipenv run python3 load.py stop \
--api_endpoints_url $NOTIFIER_API_ENDPOINT_URL \
--access_token $NOTIFIER_ACCESS_TOKEN \
--gcpid $notifier_project_id)
```

### Step 4: Loading users

We have a sample user file at `notifier/tools/samples/users.txt` with one user to be edited.
The sample user has:

* An email that will be used on email notification, both Google App engine emails and SendGrid
* A cell phone number to receive SMS notification. You may need to register this number beforehand on Twilio. Check [Twilio documentation](https://support.twilio.com/hc/en-us/articles/223180048-Adding-a-Verified-Phone-Number-or-Caller-ID-with-Twilio) to see your specific requirements.
* An Jira user Id if you are using the Jira integration. Usually it is the user login on Jira
* The User type, for example "developer". it can used to filter user from a large file so that only the ones with a single type will be uploaded.

The sample file has only one user. If you want to add more users you can copy this line to create new lines with the other users info. The order of the values on the file must be email, phone number, JiraId, type.

After editing the upload the user file:

```bash
(cd notifier/tools; \
pipenv run python3 load.py users \
--userfile ./samples/users.txt \
--gcpid $notifier_project_id \
--api_endpoints_url $NOTIFIER_API_ENDPOINT_URL \
--access_token $NOTIFIER_ACCESS_TOKEN)
```

### Step 5: Setting up the active notification channels

The valid notification channels values are:

* gae_email - Uses the GAE [Mail API](https://cloud.google.com/appengine/docs/standard/java/mail/sending-mail-with-mail-api). It is limited to 100 email each day. It is used mainly for testing/validation
* sms - Uses the [Twilio API](https://www.twilio.com/docs/libraries/java) to send SMS notifications.
* sendgrid - Uses the [SendGrid API](https://sendgrid.com/docs/for-developers/sending-email/v3-java-code-example/) the send emails
* jira - Uses the [Jira API](https://developer.atlassian.com/server/jira/platform/java-apis/) to create issues based on the messages received.

To set gae_email, sms and sendgrid as the active notification channels run:

```bash
(cd notifier/tools; \
pipenv run python3 load.py channels \
--channel 'gae_email,sms,sendgrid' \
--api_endpoints_url $NOTIFIER_API_ENDPOINT_URL \
--access_token $NOTIFIER_ACCESS_TOKEN \
--gcpid $notifier_project_id)
```

You can add only one channel, for example, 'gae_email', to validate the application before adding more channels.

### Step 6: Setting up the notification channels configuration

We use an YAML file with the setup the configuration for each channel. You just need to edit the configuration for the channels you are going to used.

The configuration file has the following sections:  

* **SMS**: for the Twilio configuration you must inform the _ACCOUNT_SID_, the _AUTH_TOKEN_ and the _FROM_NUMBER_. See the [this](https://www.twilio.com/docs/usage/your-request-to-twilio#credentials) Twilio documentation for an explanation on _ACCOUNT_SID_ and _AUTH_TOKEN_ and [this](https://www.twilio.com/docs/phone-numbers) documentation for an explanation on _FROM_NUMBER_. This number is your Twilio number.
* **SENDGRID**: for the SendGrid configuration you must inform the _API_KEY_, the _FROM_EMAIL_ and the _REPLYTO_EMAIL_. See this [SendGrid documentation](https://sendgrid.com/docs/API_Reference/Web_API_v3/How_To_Use_The_Web_API_v3/authentication.html) to get the _API_KEY_. You can put any valid email from you organization on the _FROM_EMAIL_ and _REPLYTO_EMAIL_.
* **GAE_EMAIL**: for the GAE email configuration you must inform the _FROM_EMAIL_. See this [GAE documentation](https://cloud.google.com/appengine/docs/standard/java/mail/?hl=en_US&_ga=2.190241003.-1396446243.1528827178#Java_Sending_mail) on the restrictions on the email value. You also need to register the _FROM_EMAIL_ as a valid mail sender at the [console](https://console.cloud.google.com/appengine/settings/emailsenders)
* **JIRA**: for the Jira configuration you must inform the _URL_, the _PROJECT_KEY_, the _ISSUE_TYPE_NAME_, the _USER_NAME_ and the _API_TOKEN_. See [this documentation](https://confluence.atlassian.com/cloud/api-tokens-938839638.html) on how to get an _API_TOKEN_.
  * The _URL_ in in the format https://jiraexample.atlassian.net
  * The _PROJECT_KEY_ is the project key, like TEST.
  * The _ISSUE_TYPE_NAME_ is one of Bug, Epic, Story, Task
  * The _USER_NAME_ is the user configured for access to the project. The _API_TOKEN_ will be created for this user

There is also an additional channel configuration on the file with is related to using a cloud function as a channel.

For the **CLOUD_FUNCTION** channel you need to inform the _URL_ and the _CLIENT_KEY_. We have a sample cloud function deployed with the **Notifier** Application. The _CLIENT_KEY_ value is on the cloud function configuration file at `notifier/function/default/config.json`  and the _URL_ is:

```bash
# the project created to install the application
export notifier_project_id=<your_notifier_project_id>

# one region listed in
# [Cloud Functions Locations](https://cloud.google.com/functions/docs/locations)
export region=<your_region>

echo https://${region}-${notifier_project_id}.cloudfunctions.net/notifier_notifyDefaultHttp
```

The sample cloud function deployed logs the notification received and then return an `Notification accepted.` message.

To upload the configuration YAML after you have edited run:

```bash
(cd notifier/tools; \
pipenv run python3 load.py config \
--config ./samples/configuration.yaml \
--gcpid $notifier_project_id \
--access_token $NOTIFIER_ACCESS_TOKEN \
--api_endpoints_url $NOTIFIER_API_ENDPOINT_URL)
```

### Step 7: Loading rules

We have a set of rules to decide if a notification should be sent by type the resource: _Asset_ or _Finding_ and by type of action upon the resource: _ANY-CREATED_, _ANY-DELETED_, _ANY-ACTIVE_, _ANY-OPENED_, _ANY-RESOLVE_ and _ALL_

The sample YAML file `notifier/tools/samples/rules.yaml` if configured to sent notification in all cases and can be used as an starting point.

```bash
(cd notifier/tools; \
pipenv run python3 load.py rules \
--yaml_file ./samples/rules.yaml \
--gcpid $notifier_project_id \
--access_token $NOTIFIER_ACCESS_TOKEN \
--api_endpoints_url $NOTIFIER_API_ENDPOINT_URL)
```

### Step 8: Loading custom message info text

You can add a custom message info text to the notification using this script:

```bash
export msg_text1 ="This notification is confidential."
export msg_text2 ="If you received it in error please notify the system administrator."

(cd notifier/tools; \
pipenv run python3 load.py extra_info \
--notitype ASSETS \
--message "${msg_text1}${msg_text12}" \
--api_endpoints_url $NOTIFIER_API_ENDPOINT_URL \
--access_token $NOTIFIER_ACCESS_TOKEN \
--gcpid ${notifier_project_id})
```

This custom message info text will be added to all the messages and can be used to add some custom information to the message, be it a disclaimer, some contact information or any other relevant info for the user that will receive the message.

### Step 9: Start processing messages

```bash
(cd notifier/tools; \
pipenv run python3 load.py start \
--api_endpoints_url $NOTIFIER_API_ENDPOINT_URL \
--access_token $NOTIFIER_ACCESS_TOKEN \
--gcpid ${notifier_project_id})
```

**Note:** _The Notifier Application keeps tracks of assets and findings that had already been sent from a given query so that they will not be sent again. This behavior can be change at the deploy of the application adding the parameter --notifier_hash_mecanism OFF on the call to the `run_setup_notifier.py` script. You can also go to the [console](https://console.cloud.google.com/datastore/entities;kind=AssetHash;ns=notifier/query/kind) and delete the hashes._

# Connecting **Notifier** Application with **Creator** Application

If you have deployed the **Creator** Application, a topic named  `publish_processing` was created during **Creator** Application setup process on the Creator project.

You will need to create a subscription on the `publish_processing` topic that will push messages to the **Notifier** Application. You need the **Pub/Sub Admin** role on the creator project to run the script.

```bash
export creator_project_id=<your-creator-project>
(cd setup; \
export notifier_pubsub_path=https://${notifier_project_endpoint}-pubsub-dot-${notifier_project_id}; \
export notifier_push_endpoint=${notifier_pubsub_path}.appspot.com/_ah/push-handlers/receive_message; \
pipenv run python3 add_subscription.py \
--topic_name publish_processing \
--topic_project ${creator_project_id} \
--subscription_project ${notifier_project_id} \
--subscription_name publishprocessing-notifier \
--push_endpoint ${notifier_push_endpoint})
```

Now a query that use the topic `publish_processing` or don't inform a topic and use the default topic will sent notification to the  **Notifier** Application.