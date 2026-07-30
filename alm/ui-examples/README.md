<!--
Copyright 2026 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# ALM UI Samples

This directory contains a sample Flask application intended to be run under App Lifecycle Management (ALM).

## Setup

First, activate your virtual environment and run the application locally:

```bash
source .venv/bin/activate
python app.py
```

## Deployment

To deploy this containerized application to Artifact Registry, execute the following commands.
Ensure that you replace `your-project-id` and `your-region` with your actual Google Cloud Project ID and region!

```bash
export _REGION="your-region"
export _PREFIX="region-deployment"
export _projectID="your-project-id"
export _version="v2.01.0"

# Create the Artifact Registry repository
gcloud artifacts repositories create ${_PREFIX} \
    --repository-format=docker \
    --location=$_REGION \
    --project=${_projectID}

# Build the docker container
docker build --tag ${_REGION}-docker.pkg.dev/${_projectID}/${_PREFIX}/${_version}:latest .

# Push the docker container to Artifact Registry
docker push ${_REGION}-docker.pkg.dev/${_projectID}/${_PREFIX}/${_version}:latest
```
