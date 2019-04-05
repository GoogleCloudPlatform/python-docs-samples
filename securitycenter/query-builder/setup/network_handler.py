import os
from commands import static_ip_exists
from datetime import datetime
import helpers as helpers
from base import (run_command)


def create_network_infra(project_id, region, network_input, use_dm=False):
    """
    Create network with given sub-network and static IP (if does not exist yet).
    :param network_name: network name
    :param project: project id
    :param region: GCP compute region
    :param static_ip: static IP name
    :param sub_network_name: sub-network name
    :return:
    """
    static_ip_created = False

    if use_dm:
        nw_template = os.path.join(helpers.BASE_DIR, 'dm', 'gke_nw.py')
        cmd = [
            'gcloud', 'deployment-manager', 'deployments', 'create',
            '-'.join(['dm', 'nw', project_id,
                    datetime.utcnow().strftime('%Y%m%d%H%M%S')]),
            '--template', nw_template,
            '--properties',
            ",".join([
                'region:' + region,
                'network:' + network_input.network_name,
                'subnetwork:' + network_input.sub_network_name,
                'subnet_range_1:' + network_input.subnet_range_1,
                'subnet_range_pods:' + network_input.subnet_range_pods,
                'subnet_range_services:' + network_input.subnet_range_services
            ]),
            '--project', project_id
        ]
        run_command(cmd)
    else:
        cmd = [
            'gcloud', 'compute', 'networks', 'create',
            network_input.network_name,
            '--project "{}"'.format(project_id)
        ]
        run_command(cmd)

        cmd = [
            'gcloud', 'compute', 'networks', 'subnets', 'create',
            network_input.sub_network_name,
            '--network "{}"'.format(network_input.network_name),
            '--region "{}"'.format(region),
            '--range "{}"'.format(network_input.subnet_range_1),
            '--enable-private-ip-google-access',
            '--secondary-range={}-pods={},{}-services={}'.format(network_input.sub_network_name, network_input.subnet_range_pods, network_input.sub_network_name, network_input.subnet_range_services),
            '--project "{}"'.format(project_id)
        ]
        run_command(cmd)

    if not static_ip_exists(network_input.static_ip, project_id):
        cmd = [
            'gcloud', 'compute', 'addresses', 'create',
            network_input.static_ip, '--global',
            '--project', project_id
        ]
        run_command(cmd)
        static_ip_created = True
    return static_ip_created
