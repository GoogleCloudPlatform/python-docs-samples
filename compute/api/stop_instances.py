from pprint import pprint
import googleapiclient.discovery
from oauth2client.client import GoogleCredentials
import os

#Python script to stop the running servers
instance_action = os.getenv('ACTION') #action to be done exp: stop
project_id= os.getenv('GCP_PROJECT_ID') #type project name in env variable 

#function to stop the running servers
def execute_instance_action():
    # Get list of zone in project
    zone_list = []
    gce_instances = []
    # Use default credentials
    credentials = GoogleCredentials.get_application_default()
    # Build and initialize the API
    compute_client = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)
    # Execute action on instances with the specified label key values
    zone_result = compute_client.zones().list(project=project_id).execute()
    for zone_rows in zone_result['items']:
        zone_list.append(zone_rows['name'])
    for zone_name in zone_list:
        # For every zone get the instance details
        instances_result = compute_client.instances().list(project=project_id, zone=zone_name, filter='status=RUNNING').execute()
        if 'items' in instances_result:
            for instance_row in instances_result["items"]:
                instance_name = instance_row["name"]
                instance_zone = zone_name
                gce_instances.append(instance_name)
                action_api_call = "compute_client.instances()."+instance_action+\
                "(project=project_id, zone=instance_zone, instance=instance_name)" #instance_action value will be added here like stop 
                action_result = eval(action_api_call).execute()

def main():
    # Use default credentials
    credentials = GoogleCredentials.get_application_default()
    # Build and initialize the API
    compute_client = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)
    # Execute action on instances with the specified label key values
    execute_instance_action(compute_client,instance_action)
if __name__ == "__main__":
    main()
