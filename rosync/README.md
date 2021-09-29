# rosync
It rotates user-managed service account keys in the google cloud platform and syncs them in Github secrets.

## Problem?
The use of a static user-managed service account key is dangerous and can lead to fatal security-related issues.

## Solution
There are many solutions. For example, [workload identity federation](https://cloud.google.com/iam/docs/workload-identity-federation) where you can provide access without using the service account key or vault from the HashiCorp to manage secrets and protect sensitive data, etc.

We target the set of audiences who want to use the google cloud service account keys for authentication and they want to rotate them periodically. The secret rotation itself is pretty easy to implement but we did not find any solution which syncs these newly created service account keys to Github secrets. Hence, we created "rosync".

## How it works?
It creates a new user-managed service account key and syncs it in the Github secrets. It then deletes all the outdated user-managed service account keys. If the sync is unsuccessful, it removes the newly created service account key and keeps the old keys untouched.

## How to use it?
First, clone this repository in your existing project. Afterward, you need to set the following environment variables [API_PUBLIC_KEY](https://docs.github.com/en/rest/reference/actions#get-a-repository-public-key), 
[API_SECRET](https://docs.github.com/en/rest/reference/actions#create-or-update-a-repository-secret), [GCP_PROJECT](https://cloud.google.com/resource-manager/docs/creating-managing-projects), [GIT_PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token), and [SERVICE_ACCOUNT](https://cloud.google.com/iam/docs/creating-managing-service-accounts#iam-service-accounts-create-console).
```
$ export API_PUBLIC_KEY="https://api.github.com/repos/{owner}/{repo}/actions/secrets/public-key"
$ export API_SECRET="https://api.github.com/repos/{owner}/{repo}/actions/secrets/{secret-name}"
$ export GCP_PROJECT="gcp-project-id-of-service-account"
$ export GIT_PAT="Github presonal-access-token"
$ export SERVICE_ACCOUNT="GCP service account email"
```
Here, {owner} and {repo} name are unique to each individual. Hence, please make the changes accordingly.

1. API_PUBLIC_KEY is required to get the public key and key_id of your repository. The public key is necessary to encrypt the user-managed service account key. The key_id is the id of the public key, and it is encapsulated in the payload of the PUT request to update the Github secret. 

1. API_SECRET is the API of the Github secret where you send the PUT request with an encrypted GCP service account key to update/sync it.

1. GCP_PROJECT is the GCP project ID where the SA and its keys exist.

1. GIT_PAT is the Github personal access token. It is necessary to update the Github secrets. 

1. SERVICE_ACCOUNT is the GCP service account email. It has this "my-service-account@my-gcp-project.iam.gserviceaccount.com" format. It is required to authenticate against google cloud. We will be rotating its user-managed keys and syncing them in Github secrets.

To setup the python3 virtual environment:
```
$ python3 -m pip install --upgrade pip
$ python3 -m pip install --user virtualenv
$ python3 -m venv env
$ source env/bin/activate
```

To install required dependencies:
```
$ pip install -r rosync/requirements.txt
```

To run the rosync tool:
```
$ python3 rosync/rosync.py
```

You can also use the Github Actions workflow to run it as the cron job that periodically rotates the GCP service account key and syncs it in Github secrets. Just clone this repo in your existing project and create a Github actions workflow. For example:
```
name: "Rotates GCP SA key and syncs it in Github secrets"

on:
  workflow_dispatch:
  schedule:
    - cron:  '0 */3 * * *'

jobs:
  rosync:
    name: "Rotates GCP SA key and syncs it in Github secrets"
    runs-on: [ubuntu-latest]

    steps:
    - name: Checkout
      uses: actions/checkout@v2

    - name: Set up Python 3.9
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Set up Cloud SDK
      uses: google-github-actions/setup-gcloud@master
      with:
        service_account_key: ${{ secrets.SA_KEY }}
        export_default_credentials: true

    - name: Setup and activate python virtualenv
      run: |
        rm -rf env
        python3 -m pip install --upgrade pip
        python3 -m pip install --user virtualenv
        python3 -m venv env
        source env/bin/activate

    - name: Install dependencies
      run: pip install -r rosync/requirements.txt

    - name: Rotates GCP SA key and syncs it in Github secrets
      run: python3 rosync/rosync.py
      env:
        API_PUBLIC_KEY: "https://api.github.com/repos/{owner}/{repo}/actions/secrets/public-key"
        API_SECRET: "https://api.github.com/repos/{owner}/{repo}/actions/secrets/SA_KEY"
        GCP_PROJECT: "gcp-project-id-of-service-account"
        GIT_PAT: ${{ secrets.GIT_PAT }}
        SERVICE_ACCOUNT: "my-service-account@my-gcp-project.iam.gserviceaccount.com"
```

## Questions?
If you have any questions, please write me an email at nikkytub@gmail.com
