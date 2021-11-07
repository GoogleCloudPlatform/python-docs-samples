# Automating cost controls by capping billing

## Overview

In this tutorial, you will learn to automate cost controls by setting up programmatic budget notifications. 
Programmatic budget notifications can be used to disable billing, which will stop the usage of paid services for your project. 

You may choose to disable billing if you have a hard limit on how much money you can spend on Google Cloud. 
This may be the case for students, researchers, or developers working in sandbox environments.

As you complete this guide, you will learn the following skills: 
+ Creating a budget
+ Setting up a Pub/Sub topic
+ Connecting a billing account to a Pub/Sub topic
+ Deploying a function

**Time to complete:** About 10 minutes

## Getting started 

### Before you begin

Before you attempt this tutorial, you will need:
+ An [active Cloud billing account](https://cloud.google.com/billing/docs/how-to/manage-billing-account#create_a_new_billing_account), where you are a billing admin, or you have been granted the correct level of permissions to complete the steps in this tutorial.

## Understand best practices

We recommend that you configure a separate, single Google Cloud project to contain all of your billing administration needs, including your Cloud Billing-related Pub/Sub topics. Your billing administration Google Cloud project can also be used for things like Cloud Billing Budget API access, Cloud Billing Account API access, Cloud Billing exported data, and so on.

## Select a test project 

For this tutorial, select or create a test project. The function will be acting on this project, not the billing administration project.  

**Caution:** Using the cap billing example will remove Cloud Billing from your project, shutting down all resources. This may result in resources being irretrievably deleted, with no option to recover services. You can re-enable Cloud Billing, but there is no guarantee of service recovery and manual configuration is required.

<walkthrough-project-setup></walkthrough-project-setup> 

```sh
export GOOGLE_CLOUD_PROJECT={{project_id}}
```

## Select a billing administration project

For this tutorial, create a new billing administration project.

<walkthrough-project-setup></walkthrough-project-setup> 

## Setup

Set up a default project ID so that you do not need to provide them in commands where those values are required. 

```sh   
gcloud config set project {{project-id}}  
```

Enable the Billing Budgets, Cloud Functions, Cloud Billing, and Cloud Build APIs, which you will need for this tutorial. 
```sh
gcloud services enable billingbudgets.googleapis.com cloudfunctions.googleapis.com cloudbilling.googleapis.com cloudbuild.googleapis.com
```

Set up environment variables for your budget, Pub/Sub topic, and function.
```sh
export BUDGET_NAME=billing_cap_budget
export TOPIC_NAME=budget-notification
export FUNCTION_NAME=stop_billing
``` 

**Next: Learn how to set up programmatic budget notifications**

## Set up programmatic notifications

To set up **programmatic budget notifications**, you must create a Pub/Sub topic, create a Cloud Billing budget, and connect the Cloud Billing budget to the Pub/Sub topic. 

### Create a Pub/Sub topic

Create a Pub/Sub topic so that Cloud Billing can publish budget alerts to the topic. 
```sh
gcloud pubsub topics create ${TOPIC_NAME}
```

### Connect a billing account

Find your project’s billing account ID with the following command. Copy the billing account ID. 

**Note:** If you don’t see a billing account ID, make sure your project is attached to a billing account.
```sh
gcloud beta billing projects describe {{project-id}} | grep billingAccountName
```

Replace <BILLING_ID> with your project’s billing account ID. 
```sh
export BILLING_ACCOUNT=<BILLING_ID>
```
**Next: Learn how to create a budget**

## Create a budget

Create a test budget of $100 that is associated with your project’s billing account. This command also specifies the Pub/Sub topic where budget related messages will be sent. 
```sh
gcloud alpha billing budgets create \
--billing-account=${BILLING_ACCOUNT} \
--display-name=${BUDGET_NAME} \
--budget-amount=100 \
--all-updates-rule-pubsub-topic="projects/${GOOGLE_CLOUD_PROJECT}/topics/${TOPIC_NAME}"
```

**Next: Learn more about the cap billing function and how to deploy it**

## Deploy the function

This function will remove the billing account associated with the project if the cost amount is higher than the budget amount. 
```sh
gcloud functions deploy ${FUNCTION_NAME} \
--runtime=python37 \
--source=./sample_code \
--trigger-topic=${TOPIC_NAME}
```

**Next: Learn about service account permissions and how to configure them**

## Configure service account permissions

During the creation, updating, or deletion of a function, the Cloud Functions service uses the Google Cloud Functions service agent service account. You must grant the service account the proper permissions so that it can disable billing, such as the Billing Admin role. 
```sh
gcloud projects add-iam-policy-binding \
${GOOGLE_CLOUD_PROJECT} \
--member='serviceAccount:'${GOOGLE_CLOUD_PROJECT}'@appspot.gserviceaccount.com' \
--role='roles/owner'
```
**Next: Verify that Cloud Billing is disabled**

## Verify that Cloud Billing is disabled

To disable Cloud Billing on your project, publish a sample message in Pub/Sub with the test message below. If successful, the project will no longer be visible under the billing account and resources in the project will be disabled. 
```sh
gcloud pubsub topics publish ${TOPIC_NAME} --message='{"costAmount": 100.01,"budgetAmount": 100.00}'
```

Check that your billing account has been removed with this command. If the output is blank, then you have successfully disabled Cloud Billing. 
```sh
gcloud beta billing projects describe {{project-id}} | grep billingAccountName
```

**Next: Wrapping up** 

## Congratulations!

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

You’ve completed the Cap Billing walkthrough! 

**What's Next** 

Here are some areas to explore to learn more about automating cost controls:
+ [Sending notifications to Slack](https://cloud.google.com/billing/docs/how-to/notify#send_notifications_to_slack)
+ [Selectively controlling usage of resources](https://cloud.google.com/billing/docs/how-to/notify#selectively_control_usage)