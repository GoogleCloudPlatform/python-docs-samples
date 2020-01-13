# cloud-trace-demo-app

Public Docker image: gcr.io/another-gke-demo/final-demo-image

Open this demo app in [Google Cloud Shell](https://cloud.google.com/shell/docs/). This includes necessary tools.

[![Open Cloud Trace Demo APP in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?cloudshell_git_repo=https://github.com/ZiweiZhao/cloud-trace-demo-app.git&amp;cloudshell_tutorial=README.md)

Run `gcloud init` to set up your region and zone.

#### If you are using cloud shell, skip following steps.

1. Install gcloud https://cloud.google.com/sdk/install
2. Install kubectl https://kubernetes.io/docs/tasks/tools/install-kubectl/
3. Install docker https://docs.docker.com/install/

#### If you are using an existing image we provide, skip following steps.

4. Build Image:
    `sudo docker build -t gcr.io/${PROJECT-ID}/cloud-trace-demo .`
5. Upload Image to Container Registry:
    `sudo gcloud docker -- push gcr.io/${PROJECT-ID}/cloud-trace-demo-test:v1`
    
Note: Learn how to find your project id: https://support.google.com/googleapi/answer/7014113?hl=en

#### Create your GKE cluster
6. Enable Google cloud and set up regions
    `gcloud init`
7. Enable GKE api & billing: 
    `gcloud services enable container.googleapis.com`
8. Create GKE cluster:
    `gcloud container clusters create ${CLUSTER-NAME}`
    
#### Send Requests to see generated Traces

9. Run setup.sh to apply the YAML files. Note this file configures the default image we provide.
    `./setup.sh`
10. Send request to the last service: 
    `curl $(kubectl get svc cloud-trace-demo-a -ojsonpath='{.status.loadBalancer.ingress[0].ip}')`
11. Visit https://pantheon.corp.google.com/projectselector2/traces/ to check traces generated
12. Clean up GKE cluster/pods/services 
    `gcloud container clusters delete ${CLUSTER-NAME}`
