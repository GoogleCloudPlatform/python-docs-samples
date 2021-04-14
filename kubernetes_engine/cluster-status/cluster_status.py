
"""
BEFORE RUNNING:
---------------
1. If not already done, enable the Cloud Resource Manager API
   and check the quota for your project at
   https://console.developers.google.com/apis/api/cloudresourcemanager
2. If not already done, enable the Kubernetes Engine API
   and check the quota for your project at
   https://console.developers.google.com/apis/api/container
3. This sample uses Application Default Credentials for authentication.
   If not already done, install the gcloud CLI from
   https://cloud.google.com/sdk and run
   `gcloud beta auth application-default login`.
   For more information, see
   https://developers.google.com/identity/protocols/application-default-credentials
4. Install the Python client library for Google APIs by running
   `pip install --upgrade google-api-python-client`
"""
from pprint import pprint
import json

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()

resource_manager_service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
gke_service = discovery.build('container', 'v1', credentials=credentials)

resource_request = resource_manager_service.projects().list()
resource_response = resource_request.execute()


for project in resource_response.get('projects', []):
    if(project["lifecycleState"]=="ACTIVE"):
        project_id = project["projectId"] 
        location = "location" # To-Do: Update placeholder value for location.
        parent = 'projects/'+project_id+'/locations/'+location
        gke_request = gke_service.projects().locations().clusters().list(parent=parent)
        gke_response = gke_request.execute()
        for cluster in gke_response.get('clusters',[]):
            cluster_name = cluster["name"]
            pprint("Cluster "+cluster["name"]+" status: "+cluster["status"])
