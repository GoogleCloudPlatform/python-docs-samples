#!/usr/bin/env python3
"""
Script that cleanup assets and infrastructure created by query_builder setup
"""

import click
import colorama

from base import run_command
from click_script_commons import (
    parse_args,
    configure_helpers,
    instruction_separator
)
from commands import (cluster_exists,
                      static_ip_exists)
from compute_handler import (
    network_exists,
    sub_network_exists,
    list_backend_services,
    delete_backend_service,
    list_target_proxies,
    delete_target_proxy,
    list_forwarding_rules,
    delete_forwarding_rules,
    list_health_checks,
    delete_health_check,
    list_url_maps,
    delete_url_maps
)
from region_validations import get_region_by_zone
from simulation_mode import simulation_wall
from sql_handler import (
    stop_instance,
    cloud_sql_instance_exists
)
from validator_handler import (validate_project, validate_zone)

colorama.init()


@click.command()
@click.option('--input-file',
              help='Input file', required=True)
@click.option('--simulation/--no-simulation',
              default=True,
              help='Simulate the execution. Do not execute any command.')
def run_cleanup(simulation, input_file):
    """ run cleanup script flow """
    with simulation_wall(simulation):
        configure_helpers(simulation)
        cleanup_input = parse_args(input_file)

        validate_arguments(cleanup_input)
        project = cleanup_input.query_builder.project_id
        zone = cleanup_input.query_builder.compute_zone
        region = get_region_by_zone(zone)
        network_name = cleanup_input.network.network_name
        sub_network_name = cleanup_input.network.sub_network_name
        gke_cluster = cleanup_input.cluster.cluster_name
        static_ip = cleanup_input.network.static_ip
        cloud_sql_instance_name = cleanup_input.cloud_sql.instance_name

        if cloud_sql_instance_exists(cloud_sql_instance_name, project):
            with instruction_separator("Cloud SQL Instance", "Stopping"):
                stop_instance(cloud_sql_instance_name, project)

        if cluster_exists(gke_cluster, project):
            with instruction_separator("GKE Cluster", "Deleting"):
                delete_gke_cluster(gke_cluster, project, zone)

        if static_ip_exists(static_ip, project):
            with instruction_separator("Static IP", "Deleting"):
                delete_static_ip(project, static_ip)

        if sub_network_exists(sub_network_name, project):
            with instruction_separator("Subnetwork", "Deleting"):
                delete_sub_network(project, region, sub_network_name)

        if network_exists(network_name, project):
            with instruction_separator("Network", "Deleting"):
                delete_network(network_name, project)

        for backend_service in list_backend_services(project):
            delete_backend_service(project, backend_service["name"])

        for target_proxy in list_target_proxies(project, "https"):
            delete_target_proxy(project, "https", target_proxy["name"])

        for target_proxy in list_target_proxies(project, "http"):
            delete_target_proxy(project, "http", target_proxy["name"])

        for forwarding_rule in list_forwarding_rules(project):
            delete_forwarding_rules(project, forwarding_rule["name"])

        for health_check in list_health_checks(project):
            delete_health_check(project, health_check["name"])

        for url_map in list_url_maps(project):
            delete_url_maps(project, url_map["name"])


def validate_arguments(cli_input):
    """Validate all needed properties for the given input"""
    check_zones(cli_input)
    check_projects(cli_input)


def check_zones(cli_input):
    """Validate all zones for the given input"""
    project_id = cli_input.query_builder.project_id
    zones = [
        cli_input.query_builder.compute_zone,
    ]
    zones = set(zones)
    for zone in zones:
        element_message = 'zone: ' + zone
        validate_zone(zone, element_message, project_id)


def check_projects(cli_input):
    """Validate query builder project id for the given input"""
    project_id = cli_input.query_builder.project_id
    element_message = 'project id: {}'.format(project_id)
    validate_project(project_id, element_message)


def delete_network(network_name, project):
    """
    Delete the following network from the respective project.
    If there's a sub-network associated, this must be removed first.
    :param network_name: created network name
    :param project: project id
    :return:
    """
    cmd = [
        'gcloud', 'compute', 'networks', 'delete', network_name,
        '--project', project,
        '--quiet'
    ]
    run_command(cmd)


def delete_sub_network(project, region, sub_network_name):
    """
    Delete the following sub-network from the respective project and compute
    region
    :param project: project id
    :param region: GCP compute region
    :param sub_network_name: created sub-network name
    :return:
    """
    cmd = [
        'gcloud', 'compute', 'networks', 'subnets', 'delete',
        sub_network_name,
        '--region', region,
        '--project', project,
        '--quiet'
    ]
    run_command(cmd)


def delete_static_ip(project, static_ip):
    """
    Delete the static IP from the respective project
    :param project: project id
    :param static_ip: name that is referenced by the static IP
    :return:
    """
    cmd = [
        'gcloud', 'compute', 'addresses', 'delete', static_ip,
        '--global',
        '--project', project,
        '--quiet'
    ]
    run_command(cmd)


def delete_gke_cluster(gke_cluster, project, zone):
    """
    Delete the following Kubernetes Cluster from the respective project and
    compute zone
    :param gke_cluster: created GKE cluster name
    :param project: project id
    :param zone: GCP compute zone
    :return:
    """
    cmd = [
        'gcloud', 'container', 'clusters', 'delete', gke_cluster,
        '--zone', zone,
        '--project', project,
        '--quiet'
    ]
    run_command(cmd)


def delete_bucket(bucket_name):
    """
    Delete the referred bucket
    :param bucket_name: name of the bucket on Cloud Storage
    :return:
    """
    cmd = [
        'gsutil', 'rb',
        'gs://' + bucket_name
    ]
    run_command(cmd)


def delete_bucket_contents(bucket_name):
    """
    Delete the referred bucket contents
    :param bucket_name: name of the bucket on Cloud Storage
    :return:
    """
    cmd = [
        'gsutil', 'rm',
        'gs://' + bucket_name + "/**"
    ]
    run_command(cmd)


if __name__ == '__main__':
    run_cleanup()  # pylint: disable=no-value-for-parameter
