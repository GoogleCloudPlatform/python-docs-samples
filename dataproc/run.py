import os
import create_cluster
import uuid

project_id = os.environ['GOOGLE_CLOUD_PROJECT']
region = 'us-central1'
cluster_name = 'test-cluster-{}'.format(str(uuid.uuid4()))

create_cluster.create_cluster(project_id, region, cluster_name)
