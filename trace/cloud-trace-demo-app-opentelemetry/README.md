# cloud-trace-demo-app-opentelemetry

Open this demo app in [Google Cloud Shell](https://cloud.google.com/shell/docs/). This includes necessary tools.

[![Open Cloud Trace Demo APP in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?cloudshell_git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=trace/cloud-trace-demo-app/README.md&amp;cloudshell_tutorial=trace/cloud-trace-demo-app/README.md)

## Demo Requirements

If you are using Cloud Shell, skip to the next section.

1. Install gcloud <https://cloud.google.com/sdk/install>
2. Install kubectl <https://kubernetes.io/docs/tasks/tools/install-kubectl/>
3. Install docker <https://docs.docker.com/install/>

## Deploy and run the demo application

1. Enable Google Cloud and set up region and zone.

   ```bash
   gcloud init
   ```

1. Enable the GKE API:

   ```bash
   gcloud services enable container.googleapis.com
   ```

1. Setup GCP project to `YOUR_PROJECT_ID`. Please, replace `YOUR_PROJECT_ID` with your GCP project id.

   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

1. Setup the location of GKE cluster and create the cluster named "cloud-trace-demo".
The example below sets the cluster's location to "us-central1" region.
You can replace the region with one which is [closer][] to you:

   ```bash
   REGION=us-central1
   gcloud container clusters create cloud-trace-demo \
       --region $REGION
   ```

1. Update GKE cluster credentials and verify access to the cluster:

   ```bash
   gcloud container clusters get-credentials cloud-trace-demo --region $REGION
   kubectl get nodes
   ```

   The output is expected to display 9 work nodes (3 nodes per each zone of the us-central1 region).
   If you selected a different region, the number of nodes can differ.

1. Download the demo application:

   ```bash
   git clone https://github.com/GoogleCloudPlatform/python-docs-samples
   cd python-docs-samples/trace/cloud-trace-demo-app-opentelemetry/
   ```

1. Setup the application:

   ```bash
   ./setup.sh
   ```

   You can provide a project id as an argument to `setup.sh` or it will use
   the project id you set in Step 3.
   The script will build the docker image of the demo application.
   Will store the image into container at `gcr.io/${PROJECT_ID}/cloud-trace-demo:v1`.
   And will deploy 3 services of the application.

1. Track the status of the deployment:

   ```bash
   kubectl get deployments
   ```

   You are supposed to see three deployments:

   * cloud-trace-demo-a
   * cloud-trace-demo-b
   * cloud-trace-demo-c

1. Send a curl request to the cloud-trace-demo-a:

   ```bash
   curl $(kubectl get svc -o=jsonpath='{.items[?(@.metadata.name=="cloud-trace-demo-c")].status.loadBalancer.ingress[0].ip}')
   ```

   You are supposed to see "Helloworld!" string to be printed as a return value.

1. Visit [Trace List](https://console.cloud.google.com/traces/list) to check traces generated.
    Click on any trace in the graph to see the Waterfall View.

    ![Screenshot](example-trace.png)

1. To clean up either [delete the project][delete-project] or only the provisioned resources:

   ```bash
   gcloud container registry delete gcr.io/$(gcloud config get-value core/project))/cloud-trace-demo:v1
   gcloud container clusters delete cloud-trace-demo --region $REGION
   ```

[closer]: https://cloud.google.com/about/locations#regions
[delete-project]: https://cloud.google.com/resource-manager/docs/creating-managing-projects#shutting_down_projects
