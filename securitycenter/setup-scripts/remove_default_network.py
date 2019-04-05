#!/usr/bin/env python3

import os
import inspect
from datetime import datetime
import click

from commands import (
    network_exists,
    get_firewall_rules
)
from simulation_mode import simulation_wall
import helpers
from base import run_command, run_command_readonly


@click.command()
@click.option('--project_id', '-p', help='The project id', required=True)
@click.option('--simulation/--no-simulation',
              default=True,
              help='Simulate the execution. Do not execute any command.')
def __run_steps(simulation, project_id):
    __helpers_config(simulation)
    with simulation_wall(simulation):
        if default_network_has_no_instances(project_id):
            remove_firewall_rules(project_id)
            remove_default_network(project_id)


def remove_default_network(project_id):
    """
    Delete default network from the respective project.
    :param project_id: project id
    :return:
    """
    if network_exists('default', project_id):
        # Delete default network
        run_command([
            'gcloud', 'compute', 'networks', 'delete', 'default',
            '--project', project_id,
            '--quiet'
        ])


def remove_firewall_rules(project_id):
    """
    Delete firewall rules from the respective project.
    :param project_id: project id
    :return:
    """
    firewall_rules = get_firewall_rules(project_id)
    for rule in firewall_rules:
        run_command([
            'gcloud', 'compute', 'firewall-rules', 'delete', rule,
            '--project', project_id,
            '--quiet'
        ])


def default_network_has_no_instances(project_id):
    """
    Check if default network has instances associated.
    :param project_id: project id
    :return: if has instances associated.
    """
    result_ = run_command_readonly([
        'gcloud', 'compute', 'instances', 'list',
        '--filter', '"networkInterfaces[].network:default"',
        '--format', 'json',
        '--project', project_id,
    ])
    return result_.decode("utf-8").strip() == '[]'


def __helpers_config(simulation):
    """ setup helper variables """
    helpers.START_TIME = datetime.utcnow().strftime('%Y%m%d%H%M')
    helpers.DRY_RUN = simulation
    helpers.BASE_DIR = os.path.join(os.path.dirname(
        os.path.abspath(inspect.stack()[0][1])), '..')


if __name__ == '__main__':
    __run_steps() # pylint: disable=no-value-for-parameter
