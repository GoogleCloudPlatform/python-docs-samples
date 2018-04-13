# Endpoints Getting Started with gRPC & Python Quickstart

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=endpoints/getting-started-grpc/README.md

It is assumed that you have a working Python environment and a Google
Cloud account and [SDK](https://cloud.google.com/sdk/) configured.

1. Install dependencies using virtualenv:

    ```bash
    virtualenv -p python3 env
    source env/bin/activate
    pip install -r requirements.txt
    ```

1. Test running the code, optional:

    ```bash
    # Run the server:
    python greeter_server.py

    # Open another command line tab and enter the virtual environment:
    source env/bin/activate

    # In the new command line tab, run the client:
    python greeter_client.py
    ```

1. The gRPC Services have already been generated. If you change the proto, or
   just wish to regenerate these files, run:

    ```bash
    python -m grpc.tools.protoc \
        --include_imports \
        --include_source_info \
        --proto_path=protos \
        --python_out=. \
        --grpc_python_out=. \
        --descriptor_set_out=api_descriptor.pb \
        helloworld.proto
    ```

1. Edit, `api_config.yaml`. Replace `MY_PROJECT_ID` with your project id.

1. Deploy your service config to Service Management:

    ```bash
    gcloud endpoints services deploy api_descriptor.pb api_config.yaml

    # Set your project ID as a variable to make commands easier:
    GCLOUD_PROJECT=<Your Project ID>

    ```

1. Also get an API key from the Console's API Manager for use in the
   client later. [Get API Key](https://console.cloud.google.com/apis/credentials)

1. Enable the Cloud Build API:

    ```bash
    gcloud services enable cloudbuild.googleapis.com
    ```

1. Build a docker image for your gRPC server, and store it in your Registry:

    ```bash
    gcloud container builds submit --tag gcr.io/${GCLOUD_PROJECT}/python-grpc-hello:1.0 .
    ```

1. Either deploy to GCE (below) or GKE (further down).

## Google Compute Engine

1. Enable the Compute Engine API:

    ```bash
    gcloud services enable compute-component.googleapis.com
    ```

1. Create your instance and ssh in:

    ```bash
    gcloud compute instances create grpc-host --image-family gci-stable --image-project google-containers --tags=http-server
    gcloud compute ssh grpc-host
    ```

1. Set some variables to make commands easier:

    ```bash
    GCLOUD_PROJECT=$(curl -s "http://metadata.google.internal/computeMetadata/v1/project/project-id" -H "Metadata-Flavor: Google")
    SERVICE_NAME=hellogrpc.endpoints.${GCLOUD_PROJECT}.cloud.goog
    ```

1. Pull your credentials to access Container Registry, and run your gRPC server
   container:

    ```bash
    /usr/share/google/dockercfg_update.sh
    docker run --detach --name=grpc-hello gcr.io/${GCLOUD_PROJECT}/python-grpc-hello:1.0
    ```

1. Run the Endpoints proxy:

    ```bash
    docker run --detach --name=esp \
        --publish=80:9000 \
        --link=grpc-hello:grpc-hello \
        gcr.io/endpoints-release/endpoints-runtime:1 \
        --service=${SERVICE_NAME} \
        --rollout_strategy=managed \
        --http2_port=9000 \
        --backend=grpc://grpc-hello:50051
    ```

1. Back on your local machine, get the external IP of your GCE instance:

    ```bash
    gcloud compute instances list
    ```

1. Run the client:

    ```bash
    python greeter_client.py --host=<IP of GCE Instance>:80 --api_key=<API Key from Console>
    ```

1. Cleanup:

    ```bash
    gcloud compute instances delete grpc-host
    ```

### Google Kubernetes Engine

1. Create a cluster. You can specify a different zone than us-central1-a if you
   want:

    ```bash
    gcloud container clusters create my-cluster --zone=us-central1-a
    ```

1. Edit `deployment.yaml`. Replace `SERVICE_NAME` and `GCLOUD_PROJECT` with your values:

   `SERVICE_NAME` is equal to hellogrpc.endpoints.GCLOUD_PROJECT.cloud.goog,
   replacing GCLOUD_PROJECT with your project ID.

1. Deploy to GKE:

    ```bash
    kubectl create -f ./deployment.yaml
    ```

1. Get IP of load balancer, run until you see an External IP:

    ```bash
    kubectl get svc grpc-hello
    ```

1. Run the client:

    ```bash
    python greeter_client.py --host=<IP of GKE LoadBalancer>:80 --api_key=<API Key from Console>
    ```

1. Cleanup:

    ```bash
    gcloud container clusters delete my-cluster --zone=us-central1-a
    ```
