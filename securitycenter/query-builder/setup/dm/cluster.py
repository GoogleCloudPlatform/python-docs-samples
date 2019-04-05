"""Create configuration to deploy GKE cluster."""


def GenerateConfig(context):
    """Create configuration to deploy GKE cluster."""
    cluster_name = context.properties['cluster_name']
    cluster_version = context.properties['cluster_version']
    project_id = context.properties['k8s_project_id']
    node_pool_name = context.properties['node_pool_name']
    zone = context.properties['zone']
    cluster_ip = context.properties['cluster_ip']
    network = context.properties['network']
    subnetwork = context.properties['subnetwork']
    machine_type = context.properties['machine_type']
    min_nodes = context.properties['min_nodes']
    max_nodes = context.properties['max_nodes']

    resources = [{
        'name': cluster_name,
        'type': 'gcp-types/container-v1beta1:projects.locations.clusters',
        "properties": {
            "cluster": {
                "name": cluster_name,
                "masterAuth": {
                    "username": "admin"
                },
                "loggingService": "logging.googleapis.com",
                "monitoringService": "monitoring.googleapis.com",

                "addonsConfig": {
                    "horizontalPodAutoscaling": {
                        "disabled": False
                    },
                    "httpLoadBalancing": {
                        "disabled": False
                    }
                },
                "initialClusterVersion": cluster_version,
                "clusterIpv4Cidr": cluster_ip,

                "network": network,
                "subnetwork": subnetwork,

                "nodePools": [
                    {
                        "name": node_pool_name,
                        "initialNodeCount": 1,
                        "autoscaling": {
                            "enabled": True,
                            "minNodeCount": min_nodes,
                            "maxNodeCount": max_nodes
                        },
                        "management": {
                            "autoRepair": True,
                            "autoUpgrade": True
                        },
                        "config": {
                            "imageType": "COS",
                            "machineType": machine_type,
                            "diskSizeGb": 100,
                            "diskType": "pd-ssd",
                            "oauthScopes": [
                                "https://www.googleapis.com/auth/devstorage.read_only",
                                "https://www.googleapis.com/auth/logging.write",
                                "https://www.googleapis.com/auth/monitoring",
                                "https://www.googleapis.com/auth/servicecontrol",
                                "https://www.googleapis.com/auth/service.management.readonly",
                                "https://www.googleapis.com/auth/trace.append"
                            ]
                        },
                    }

                ]
            },
            "parent": "projects/{}/locations/{}".format(project_id, zone)
        }
    }]
    return {'resources': resources}
