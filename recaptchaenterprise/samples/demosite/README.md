# Google Cloud reCAPTCHA Enterprise

Google [Cloud reCAPTCHA Enterprise](https://cloud.google.com/recaptcha-enterprise) helps protect your website from fraudulent activity, spam, and abuse without creating friction.

This application demonstrates how to use integrate your client and server code with reCAPTCHA Enterprise - Python Client libraries.

## Prerequisites

### Google Cloud Project

Set up a Google Cloud project. 
Billing information is **not needed** to deploy this application.

# One-click deploy

1. Click the below "Open in Cloud Shell" button.

<a href="https://shell.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/googleapis/python-recaptcha-enterprise&cloudshell_git_branch=demosite-app">
<img alt="Open Cloud Shell" src ="http://gstatic.com/cloudssh/images/open-btn.png"></a>

2. Run
```
cd samples/demosite/app && export GCLOUDSDK_PYTHON=python2 && . init.sh
```

3. Click on the localhost link in the terminal output. You'll find the deployed application.


# Manual Deploy

### 1. Enable the reCAPTCHA Enterprise API

You must [enable the Google reCAPTCHA Enterprise API](https://console.cloud.google.com/flows/enableapi?apiid=recaptchaenterprise.googleapis.com) for your project in order to use this application.

### 2. Create Score key and Checkbox key

Create a Score key, and a Checkbox key via [Cloud Console.](https://console.cloud.google.com/security/recaptcha)

### 3. Set Environment Variables

Open the CloudShell from Cloud Console.
Set your project ID and site keys.

```angular2html
export GOOGLE_CLOUD_PROJECT="<google-project-id-here>"
export SITE_KEY="<score-key-id-here>"
export CHECKBOX_SITE_KEY="<checkbox-key-id-here>"
```

### 4. Clone, Build and Run

The following instructions will help you prepare your development environment.


1. Clone the python-recaptcha-enterprise repository and navigate to ```samples/demosite``` directory.

```
cloudshell_open --repo_url "https://github.com/googleapis/python-recaptcha-enterprise.git" --dir "samples/demosite" --page "shell" --force_new_clone
```

2. Run docker-compose

```
/usr/local/bin/docker-compose -f $PWD/samples/demosite/docker-compose.yaml up --build
```

3. Click on the localhost link in the terminal output. You'll find the deployed application.



### **Troubleshooting**: If you encounter a Python library not found error, try running the below command

```angular2html
export CLOUDSDK_PYTHON=python2
```

## Authentication

The above _**one-click**_ and _**manual**_ deployment works with the default **compute-engine** service account in the project. 
If you want to create a new service account, follow the below steps.

### 1. Create Service account

A service account with private key credentials is required to create signed bearer tokens.

Create
1. [Service account](https://console.cloud.google.com/iam-admin/serviceaccounts/create)
2. [Key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#iam-service-account-keys-create-console) for the service account
3. Download the key credentials file as JSON.

### 2. Grant Permissions

You must ensure that the [user account or service account](https://cloud.google.com/iam/docs/service-accounts#differences_between_a_service_account_and_a_user_account) you used to authorize your gcloud session has the proper permissions to edit reCAPTCHA Enterprise resources for your project. In the Cloud Console under IAM, add the following roles to the project whose service account you're using to test:

* reCAPTCHA Enterprise Agent
* reCAPTCHA Enterprise Admin

More information can be found in the [Google reCAPTCHA Enterprise Docs](https://cloud.google.com/recaptcha-enterprise/docs/access-control#rbac_iam).

### 3. Export the Service account credentials

```angular2html
export GOOGLE_APPLICATION_CREDENTIALS="<path-to-service-account-credentials-file>"
```
