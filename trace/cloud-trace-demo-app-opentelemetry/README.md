# cloud-trace-demo-app-opentelemetry

Open this demo app in [Google Cloud Shell](https://cloud.google.com/shell/docs/). This includes necessary tools.


[![Open Cloud Trace Demo APP in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?cloudshell_git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=trace/cloud-trace-demo-app/README.md&amp;cloudshell_tutorial=trace/cloud-trace-demo-app/README.md)

#### Demo Requirements
If you are using Cloud Shell, skip to the next section.

1. Install gcloud <https://cloud.google.com/sdk/install>
2. Install kubectl <https://kubernetes.io/docs/tasks/tools/install-kubectl/>
3. Install docker <https://docs.docker.com/install/>

    
#### Create a GKE cluster

4. Enable Google Cloud and set up region and zone.

    `gcloud init`
5. Enable the GKE API & billing:

    `gcloud services enable container.googleapis.com`
6. Create a GKE cluster named "cloud-trace-demo", replacing `your-gcp-zone`  below
with the 
[GCP Zone](https://cloud.google.com/compute/docs/regions-zones) closest in proximity to you:

     ```
     gcloud container clusters create cloud-trace-demo\`
     --num-nodes 1 \
     --enable-basic-auth \
     --issue-client-certificate \
     --zone your-gcp-zone
     ```
7. Verify that you have access to the cluster:
    
    `kubectl get nodes`

#### Deploy The Cloud Trace Demo App

8. Build and tag the docker image for demo app:

    `docker build -t gcr.io/${PROJECT_ID}/cloud-trace-demo:v1 .`
9. Deploy resource to the cluster:

    `kubectl apply -f deployment.yaml`
10. Track the status of the deployment:

    `kubectl get deployments`
    
    Deployment is complete when all of the available deployments are ready. 
11. Run the following command to see the pods the deployment created:
    
    `kubectl get pods`  

#### Deploy The Cloud Trace Demo Service

12. Create the cloud trace demo service:
    
    `kubectl apply -f service.yaml`
13. Get the services IP address by running the following command:
    
    `kubectl get services`
14. Send a curl request to the EXTERNAL_IP, replacing `EXTERNAL_IP` with the external IP address found
in step 13:
    
    `curl EXTERNAL_IP`
15. Visit [Trace List](https://console.cloud.google.com/traces/list) to check traces generated.
    Click on any trace in the graph to see the Waterfall View.
    
    ![Screenshot](example-trace.png)
16. Clean up GKE cluster/pods/services:

    `gcloud container clusters delete cloud-trace-demo`
