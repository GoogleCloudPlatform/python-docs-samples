""""K8s Cluster setup methods"""

import logging
import os
from datetime import datetime

import helpers
from base import run_command, run_command_readonly

LOGGER = logging.getLogger(__name__)


def create_cluster(project_id, zone, cluster_input, network_input, use_dm=False):
    """Create k8s cluster"""
    deployment_name = '-'.join([
        'dm',
        'cluster',
        project_id,
        datetime.utcnow().strftime('%Y%m%d%H%M%S')
    ])

    cluster_template = os.path.join(helpers.BASE_DIR, 'dm', 'cluster.py')
    cluster_versions = get_cluster_version(project_id, zone)

    if use_dm:
        cmd = [
            'gcloud', 'deployment-manager', 'deployments', 'create',
            deployment_name,
            '--template', cluster_template,
            '--properties',
            ",".join([
                'k8s_project_id:' + project_id,
                'zone:' + zone,
                'cluster_name:' + cluster_input.cluster_name,
                'cluster_version:' + cluster_versions,
                'node_pool_name:' + cluster_input.node_pool_name,
                'network:' + network_input.network_name,
                'subnetwork:' + network_input.sub_network_name,
                'cluster_ip:' + cluster_input.cluster_ip,
                'machine_type:' + cluster_input.machine_type,
                'min_nodes:' + cluster_input.min_nodes,
                'max_nodes:' + cluster_input.max_nodes
            ]),
            '--project', project_id
        ]
    else:
        cmd = [
            'gcloud', 'beta', 'container', 'clusters', 'create',
            cluster_input.cluster_name,
            '--zone "{}"'.format(zone),
            '--cluster-version "{}"'.format(cluster_versions),
            '--username "admin"',
            '--machine-type "{}"'.format(cluster_input.machine_type),
            '--image-type "COS"',
            '--disk-type "pd-ssd"',
            '--disk-size "100"',
            '--scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append"',
            '--enable-autoscaling',
            '--min-nodes={}'.format(cluster_input.min_nodes),
            '--max-nodes={}'.format(cluster_input.max_nodes),
            '--network "{}"'.format(network_input.network_name),
            '--subnetwork "{}"'.format(network_input.sub_network_name),
            '--cluster-ipv4-cidr "{}"'.format(cluster_input.cluster_ip),
            '--addons HorizontalPodAutoscaling,HttpLoadBalancing',
            '--enable-stackdriver-kubernetes',
            '--enable-autoupgrade',
            '--enable-autorepair',
            '--project "{}"'.format(project_id)
        ]

    run_command(cmd)


def get_cluster_version(project_id, zone):
    """Get version of GKE"""
    versions = run_command_readonly([
        'gcloud', 'container', 'get-server-config',
        '--quiet',
        '--zone', zone,
        '--project', project_id,
        '--format="value(validMasterVersions[0])"'
    ])
    return versions.decode("utf-8").splitlines()[-1]


def delete_gke_cluster(project_id, cluster_name, cluster_zone):
    """Deletes a GKE Cluster by name in a project"""
    cmd = [
        "gcloud", "container", "clusters", "delete", cluster_name,
        "--project", project_id,
        "--zone", cluster_zone
    ]
    run_command(cmd)
