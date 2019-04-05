% SCC Tools: **Hello World** User Guide
% Security Cloud Command Center Tools

\setcounter{section}{0}
\setcounter{secnumdepth}{10}
\newpage

# How to update the Cloud Function

If you change the source code for one of the cloud functions you will need to redeploy it. The following steps can help you to do that.

## Requirements

### Necessary roles

In order to update the Cloud Functions on **Hello World**, if you are not the _Project Owner_, you will need this roles:

* Viewer - `roles/viewer`
* Service Usage Admin - `roles/serviceusage.serviceUsageAdmin`
* API Keys Admin - `roles/serviceusage.apiKeysAdmin`
* Compute Storage Admin - `roles/storage.admin`
* Storage Admin - `roles/storage.admin`
* Storage Object Admin - `roles/storage.objectAdmin`
* Pub/Sub Admin - `roles/pubsub.admin`
* Cloud Functions Developer - `roles/cloudfunctions.developer`
* Service Account User - `roles/iam.serviceAccountUser`

_Note: If your user is not the **Project Owner** or don't have all of the required IAM roles, ask someone on your Organization to assign those roles to your user so you can continue with the installation process._

### Environment Variables

To update the Cloud Function you will need to set the necessary environment variables. If you made the installation of the **Hello World** application you probably have this variables already set, in any case if you need help on this task please check the section **Prepare the environment** on the **Hello World** readme. The variables you will need to update the Cloud Functions are listed bellow:

- **organization_id**
- **hello_world_project_id**
- **cf_bucket_name**

### API Key

To be able to use the SCC API correctly the function will need an API Key. This API Key was already created on the **Hello World** readme in the section **Create the API Key to communicate with SCC API**, if you follow that step you can easly export this key to a variable (if is not exported already).

## Update Cloud Function Script

If you have everything from the requirements already set just execute the following script to update your Cloud Function.

```bash
(cd hello-world/setup; \
pipenv run python3 update_cloud_function.py \
  --organization_id ${organization_id} \
  --project_id ${hello_world_project_id} \
  --bucket_name ${cf_bucket_name} \
  --cloud_function <logger|transformer> \
  --api_key ${api_key} \
  --no-simulation)
```
