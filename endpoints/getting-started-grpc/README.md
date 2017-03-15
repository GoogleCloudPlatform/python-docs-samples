# Endpoints Getting Started with gRPC & Python Quickstart

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
    python -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/helloworld.proto
    ```

1. Generate the `out.pb` from the proto file:

    ```bash
    python -m grpc_tools.protoc --include_imports --include_source_info -I protos protos/helloworld.proto --descriptor_set_out out.pb
    ```

1. Edit, `api_config.yaml`. Replace `MY_PROJECT_ID` with your project id.

1. Deploy your service config to Service Management:

    ```bash
    gcloud service-management deploy out.pb api_config.yaml
    # The Config ID should be printed out, looks like: 2017-02-01r0, remember this

    # Set your project ID as a variable to make commands easier:
    GCLOUD_PROJECT=<Your Project ID>

    # Print out your Config ID again, in case you missed it:
    gcloud service-management configs list --service hellogrpc.endpoints.${GCLOUD_PROJECT}.cloud.goog
    ```

1. Also get an API key from the Console's API Manager for use in the
   client later. (https://console.cloud.google.com/apis/credentials)

1. Enable the Cloud Build API:

    ```bash
    gcloud service-management enable cloudbuild.googleapis.com
    ```

1. Build a docker image for your gRPC server, and store it in your Registry:

    ```bash
    gcloud container builds submit --tag gcr.io/${GCLOUD_PROJECT}/python-grpc-hello:1.0 .
    ```

1. Either deploy to GCE (below) or GKE (further down).

### GCE

1. Enable the Compute Engine API:

    ```bash
    gcloud service-management enable compute-component.googleapis.com
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
    SERVICE_CONFIG_ID=<Your Config ID>
    ```

1. Pull your credentials to access Container Registry, and run your gRPC server
   container:

    ```bash
    /usr/share/google/dockercfg_update.sh
    docker run -d --name=grpc-hello gcr.io/${GCLOUD_PROJECT}/python-grpc-hello:1.0
    ```

1. Run the Endpoints proxy:

    ```bash
    docker run --detach --name=esp \
        -p 80:9000 \
        --link=grpc-hello:grpc-hello \
        gcr.io/endpoints-release/endpoints-runtime:1 \
        -s ${SERVICE_NAME} \
        -v ${SERVICE_CONFIG_ID} \
        -P 9000 \
        -a grpc://grpc-hello:50051
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

### GKE

1. Create a cluster. You can specify a different zone than us-central1-a if you
   want:

    ```bash
    gcloud container clusters create my-cluster --zone=us-central1-a
    ```

1. Edit `container-engine.yaml`. Replace `SERVICE_NAME`, `SERVICE_CONFIG_ID`,
   and `GCLOUD_PROJECT` with your values:

   `SERVICE_NAME` is equal to hellogrpc.endpoints.GCLOUD_PROJECT.cloud.goog,
   replacing GCLOUD_PROJECT with your project ID.

   `SERVICE_CONFIG_ID` can be found by running the following command, replacing
   GCLOUD_PROJECT with your project ID.

   ```bash
   gcloud service-management configs list --service hellogrpc.endpoints.GCLOUD_PROJECT.cloud.goog
   ```

1. Deploy to GKE:

    ```bash
    kubectl create -f ./container-engine.yaml
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
