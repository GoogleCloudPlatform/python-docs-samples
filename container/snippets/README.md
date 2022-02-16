# Samples

All the samples are self contained unless they are placed inside their own folders. The samples use [Application Default Credentails (ADC)](https://cloud.google.com/docs/authentication/production#automatically) to authenticate with GCP. So make sure ADC is setup correctly _(i.e. `GOOGLE_APPLICATION_CREDENTIALS` environment variable is set)_ before running the samples. Some sample might require additional python modules to be installed.

You can run samples as follows:

```python
python <sample_name.py> <arg1> <arg2> ...
```

You can run the following command to find the usage and arguments for the samples:

```python
python <sample_name.py> -h
```
```bash
# example
python quickstart.py -h

usage: quickstart.py [-h] project_id zone

positional arguments:
  project_id  Google Cloud project ID
  zone        GKE Cluster zone

optional arguments:
  -h, --help  show this help message and exit
```

### Quickstart sample
- [**quickstart.py**](quickstart.py): A simple example to list the GKE clusters in a given GCP project and zone. The sample uses the [`list_clusters()`](https://cloud.google.com/python/docs/reference/container/latest/google.cloud.container_v1.services.cluster_manager.ClusterManagerClient#google_cloud_container_v1_services_cluster_manager_ClusterManagerClient_list_clusters) API to fetch the list of cluster. 


### Long running operation sample

The following samples are examples of operations that take a while to complete.
For example _creating a cluster_ in GKE can take a while to set up the cluster
nodes, networking and configuring Kubernetes. Thus, calls to such long running
APIs return an object of type [`Operation`](https://cloud.google.com/python/docs/reference/container/latest/google.cloud.container_v1.types.Operation). We can
then use the id of the returned operation to **poll** the [`get_operation()`](https://cloud.google.com/python/docs/reference/container/latest/google.cloud.container_v1.services.cluster_manager.ClusterManagerClient#google_cloud_container_v1_services_cluster_manager_ClusterManagerClient_get_operation) API to check for it's status. You can see the
different statuses it can be in, in [this proto definition](https://github.com/googleapis/googleapis/blob/master/google/container/v1/cluster_service.proto#L1763-L1778).

- [**create_cluster.py**](create_cluster.py): An example of creating a GKE cluster _(with mostly the defaults)_. This example shows how to handle responses of type [`Operation`](https://cloud.google.com/python/docs/reference/container/latest/google.cloud.container_v1.types.Operation) that reperesents a long running operation. The example uses the python module [`backoff`](https://github.com/litl/backoff) to handle a graceful exponential backoff retry mechanism to check if the `Operation` has completed.

- [**delete_cluster.py**](delete_cluster.py): An example of deleting a GKE cluster. This example shows how to handle responses of type [`Operation`](https://cloud.google.com/python/docs/reference/container/latest/google.cloud.container_v1.types.Operation) that reperesents a long running operation.