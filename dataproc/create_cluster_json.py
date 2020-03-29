import os

from google.cloud import dataproc_v1beta2
import google.protobuf.json_format as json_format
import google.cloud.dataproc_v1beta2.proto.clusters_pb2 as clusters

def create_cluster(cluster_json_path,project_id,region):
    '''
    This function takes an external JSON with cluster configuration and creates the cluster.
    :param project_id: project id of the service account
    :param region: region where needs to be created
    :return: returns the cluster client instance
    '''
    cluster_client = dataproc_v1beta2.ClusterControllerClient(client_options={
        'api_endpoint':'{}-dataproc.googleapis.com:443'.format(region)
    })

    ##The JOSN is created under the clusterconfig folder
    with open(cluster_json_path, 'r') as f:
        cluster_json = f.read()
        cluster_config = json_format.Parse(cluster_json,clusters.Cluster())

    operation = cluster_client.create_cluster(project_id,region,cluster_config)
    result = operation.result()

    # Output a success message.
    print('Cluster created successfully : {}'.format(result.cluster_name))
    # [END dataproc_create_cluster]

if __name__=="__main__":
    project_id = 'xxxx' ## replace with project-id
    region = 'xxx' ## replace with region
    result = create_cluster(project_id,region)
    print(result)