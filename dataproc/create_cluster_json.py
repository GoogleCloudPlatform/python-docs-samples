import os

from google.cloud import dataproc_v1beta2
import google.protobuf.json_format as json_format
import google.cloud.dataproc_v1beta2.proto.clusters_pb2 as clusters

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:\\GCP\\xxxx.json"

def create_cluster(project_id,region):
    '''
    This function takes an external JSON with cluster configuration and creates the cluster.
    Currently, there are no examples available to do this and I learnt it the hard way. The
    function takes the JSON message and converts to protocol buffer message format
    :param project_id: project id of the service account
    :param region: region where needs to be created
    :return: returns the cluster client instance
    '''
    cluster_client = dataproc_v1beta2.ClusterControllerClient(client_options={
        'api_endpoint':'{}-dataproc.googleapis.com:443'.format(region)
    })

    ##The JOSN is created under the clusterconfig folder
    with open("./clusterconfig/dataproc-cluster.json") as f:
        cluster = f.read()
        cluster_message = json_format.Parse(cluster,clusters.Cluster())

    operation = cluster_client.create_cluster(project_id,region,cluster_message)
    result = operation.result()
    print('Cluster created successfully : {}'.format(result.cluster_name))
    return cluster_client

if __name__=="__main__":
    project_id = 'xxxx' ## replace with project-id
    region = 'xxx' ## replace with region
    result = create_cluster(project_id,region)
    print(result)