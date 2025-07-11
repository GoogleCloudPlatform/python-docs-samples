# Copyright 2025 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import hmac
import hashlib
import requests
import json
import logging
from google.oauth2 import service_account
from google.auth.transport.requests import Request as GoogleRequest
import google.auth
from flask import Request
from google.cloud import secretmanager
from github import Github


# --- Configuration ---
PROJECT_ID = os.environ.get('GCP_PROJECT')
LOCATION = 'us-central1' # Or your desired region
CLOUD_RUN_WORKER_POOL_NAME = os.environ.get('CLOUD_RUN_WORKER_POOL_NAME') # Your worker pool name


# GitHub specific config
GITHUB_ORG_OR_REPO = os.environ.get('GITHUB_ORG_OR_REPO', 'YOUR_ORG/YOUR_REPO') # e.g., 'my-org' or 'my-org/my-repo'
RUNNER_SCOPE = os.environ.get('RUNNER_SCOPE', 'repo') # 'org' or 'repo'


# Autoscaling parameters
MAX_RUNNERS = int(os.environ.get('MAX_RUNNERS', 5)) # Max number of concurrent runners
IDLE_TIMEOUT_MINUTES = int(os.environ.get('IDLE_TIMEOUT_MINUTES', 15)) # How long to wait before scaling down idle runners


# Initialize GitHub client
github_client = None
github_entity = None
try:
   # Get GH_TOKEN from Secret Manager
   client = secretmanager.SecretManagerServiceClient()
   secret_name = f"projects/{PROJECT_ID}/secrets/GH_TOKEN/versions/latest"
   response = client.access_secret_version(request={"name": secret_name})
   gh_token = response.payload.data.decode("UTF-8")
   github_client = Github(gh_token)


   if RUNNER_SCOPE == 'org':
       github_entity = github_client.get_organization(GITHUB_ORG_OR_REPO)
   else:
       owner, repo_name = GITHUB_ORG_OR_REPO.split('/')
       github_entity = github_client.get_user(owner).get_repo(repo_name)
except Exception as e:
   logging.error(f"Failed to initialize GitHub client or access GH_TOKEN: {e}")


def get_authenticated_request():
   """Returns a requests.Session object authenticated for Google Cloud APIs."""
   credentials, project = google.auth.default()
   scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
   auth_req = GoogleRequest()
   scoped_credentials.refresh(auth_req)
   return auth_req, scoped_credentials.token


def get_current_worker_pool_instance_count():
   """
   Retrieves the current manualInstanceCount of the Cloud Run worker pool.
   Returns the instance count as an integer, or -1 if retrieval fails.
   """
   auth_req, access_token = get_authenticated_request()
   if not access_token:
       logging.error("Failed to retrieve Google Cloud access token to get current instance count.")
       return -1


   url = f"https://run.googleapis.com/v2/projects/{PROJECT_ID}/locations/{LOCATION}/workerPools/{CLOUD_RUN_WORKER_POOL_NAME}"


   headers = {
       "Content-Type": "application/json",
       "Authorization": f"Bearer {access_token}"
   }


   try:
       response = auth_req.session.get(url, headers=headers)
       response.raise_for_status()
       worker_pool_data = response.json()
       current_instance_count = worker_pool_data.get('scaling', {}).get('manualInstanceCount', 0)
       logging.info(f"Current worker pool instance count: {current_instance_count}")
       return current_instance_count
   except requests.exceptions.RequestException as e:
       logging.error(f"Error getting Cloud Run worker pool details: {e}")
       if response is not None:
           logging.error(f"Response Status Code: {response.status_code}")
           logging.error(f"Response Text: {response.text}")
       return -1


def update_runner_vm_instance_count(instance_count: int):
   """
   Updates a Cloud Run worker pool with the specified instance count.
   """
   auth_req, access_token = get_authenticated_request()
   if not access_token:
       print("Failed to retrieve Google Cloud access token. Exiting.")
       return


   url = (f"https://run.googleapis.com/v2/projects/{PROJECT_ID}/locations/{LOCATION}/workerPools/"
          f"{CLOUD_RUN_WORKER_POOL_NAME}?updateMask=scaling.manualInstanceCount")
   headers = {
       "Content-Type": "application/json",
       "Authorization": f"Bearer {access_token}"
   }
   payload = {
       "scaling": {
           "scalingMode": "MANUAL",
           "manualInstanceCount": instance_count
       }
   }




   try:
       response = auth_req.session.patch(url, headers=headers, json=payload)
       response.raise_for_status()


       print(f"Successfully updated Cloud Run worker pool. Status Code: {response.status_code}")
       print("Response JSON:")
       print(json.dumps(response.json(), indent=2))


   except requests.exceptions.RequestException as e:
       print(f"Error updating Cloud Run worker pool: {e}")
       if response is not None:
           print(f"Response Status Code: {response.status_code}")
           print(f"Response Text: {response.text}")


def create_runner_vm(count: int):
   """Updates a Cloud Run worker pool to scale up to the specified count."""
   logging.info(f"Attempting to scale up Cloud Run worker pool to {count} instances.")
   update_runner_vm_instance_count(count)


def delete_runner_vm(count: int):
   """Updates a Cloud Run worker pool to scale down to the specified count."""
   logging.info(f"Attempting to scale down Cloud Run worker pool to {count} instances.")
   update_runner_vm_instance_count(count)




# --- Main Webhook Handler ---


def github_webhook_handler(request: Request):
   """
   HTTP Cloud Function that handles GitHub workflow_job events for autoscaling.
   """
   logging.getLogger().setLevel(logging.INFO) # Set logging level


   # 1. Validate Webhook Signature (IMPORTANT FOR PRODUCTION)
   # You need to implement this with your GitHub Webhook Secret.
   # This is commented out in your original code, but critical for security.
   # Example (you need to retrieve webhook_secret from Secret Manager too):
   # webhook_secret = get_secret_from_secret_manager("GITHUB_WEBHOOK_SECRET")
   # if not validate_signature(request, webhook_secret):
   #     return ("Invalid signature", 403)


   # 2. Parse Event
   event_type = request.headers.get('X-GitHub-Event')
   if event_type != 'workflow_job':
       logging.info(f"Received event type '{event_type}', ignoring.")
       return ("OK", 200)


   try:
       payload = request.get_json()
   except Exception as e:
       logging.error(f"Error parsing JSON payload: {e}")
       return ("Bad Request", 400)


   action = payload.get('action')
   job = payload.get('workflow_job')


   if not job:
       logging.warning("No 'workflow_job' found in payload.")
       return ("OK", 200)


   job_id = job.get('id')
   job_name = job.get('name')
   job_status = job.get('status') # 'queued', 'in_progress', 'completed'
   job_conclusion = job.get('conclusion') # 'success', 'failure', 'cancelled', 'skipped'


   logging.info(f"Received workflow_job event: Job ID {job_id}, Name '{job_name}', Status '{job_status}', Action '{action}'")


   # 3. Handle Scaling Logic


   current_instance_count = get_current_worker_pool_instance_count()


   if current_instance_count == -1:
       logging.error("Could not retrieve current instance count. Aborting scaling operation.")
       return ("Internal Server Error", 500)


   # Scale Up: If a job is queued and we have available capacity
   if action == 'queued' and job_status == 'queued':
       if current_instance_count < MAX_RUNNERS:
           new_instance_count = current_instance_count + 1
           logging.info(f"Job '{job_name}' is queued. Scaling up from {current_instance_count} to {new_instance_count} runners.")
           create_runner_vm(new_instance_count)
       else:
           logging.info(f"Job '{job_name}' is queued, but max runners ({MAX_RUNNERS}) reached. Current runners: {current_instance_count}.")


   # Scale Down: If a job is completed, find the corresponding runner and consider terminating it
   elif action == 'completed' and job_status == 'completed':
       # You might want more sophisticated logic here to determine which runner to shut down,
       # especially if you have multiple runners and want to only shut down idle ones.
       # For simplicity, this example scales down by one, ensuring it doesn't go below zero.
       if current_instance_count > 0:
           new_instance_count = current_instance_count - 1
           logging.info(f"Job '{job_name}' completed. Scaling down from {current_instance_count} to {new_instance_count} runners.")
           delete_runner_vm(new_instance_count)
       else:
           logging.info(f"Job '{job_name}' completed, but no runners are currently active to scale down.")
   else:
       logging.info(f"Workflow job event for '{job_name}' with action '{action}' and status '{job_status}' did not trigger a scaling action.")


   return ("OK", 200)
