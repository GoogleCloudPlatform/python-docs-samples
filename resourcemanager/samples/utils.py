from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials
import httplib2

def build_client():
    return build('cloudresourcemanager',
                 'v1beta1',
                 credentials=GoogleCredentials.get_application_default()
                 http=httplib2.Http(timeout=90) #Long timeout for create requests

def wait_for_active(project):
    timeout=1
    while project['lifecycleState'] != 'ACTIVE':
        sleep(timeout)
        timeout=timeout*2
        project = client.projects().get(projectId=project_id).execute()
    return project
