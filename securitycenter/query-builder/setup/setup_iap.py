#!/usr/bin/env python3

import os
import inspect
from datetime import datetime
import click

from simulation_mode import simulation_wall
import helpers
from base import run_command, run_command_readonly
from commands import get_project_number
from compute_handler import (    
    get_backend_service,
    get_backend_service_id
)


@click.command()
@click.option('--project_id', '-p', help='The project id', required=True)
@click.option('--oauth_client_secret', '-ocs', help='Oauth client secret',
              required=True)
@click.option('--oauth_client_id', '-oci', help='Oauth client id',
              required=True)
@click.option('--timeout',
              default=3600,
              help='The amount of time to wait in seconds for the load balancer to proxy the response to the client before considering the request failed.')
@click.option('--simulation/--no-simulation',
              default=True,
              help='Simulate the execution. Do not execute any command.')
def __run_steps(simulation,
                oauth_client_id,
                oauth_client_secret,
                project_id,
                timeout):
    __helpers_config(simulation)
    with simulation_wall(simulation):
        setup_iap(project_id, oauth_client_id, oauth_client_secret, timeout)


def setup_iap(project_id, oauth_client_id, oauth_client_secret, timeout):
    """
    Turn on IAP
    :param project_id: The project id
    :param oauth_client_id: Oauth client id
    :param oauth_client_secret: Oauth client secret
    :return:
    """
    # Turn on IAP for frontend
    __setup(project_id, oauth_client_id, oauth_client_secret,
            'description~frontend', timeout)
    # Turn on IAP for load balance
    __setup(project_id, oauth_client_id, oauth_client_secret,
            'description~default-http-backend', timeout)
    # Add Audience to validate IAP header as configmap
    __add_audience(project_id, 'description~frontend')


def __setup(project_id,
            oauth_client_id,
            oauth_client_secret,
            backend_service_filter,
            timeout):
    backend_service = get_backend_service(project_id, backend_service_filter)
    run_command([
        'gcloud', 'compute', 'backend-services',
        'update', backend_service,
        '--timeout={}'.format(
            timeout
        ),
        '--global',
        "--iap=enabled,oauth2-client-id={},oauth2-client-secret={}".format(
            oauth_client_id,
            oauth_client_secret
        ),
        '--project', project_id
    ])


def __add_audience(project_id, backend_service_filter):
    backend_service_id = get_backend_service_id(project_id,
                                                backend_service_filter)
    project_number = get_project_number(project_id)
    run_command([
        'kubectl', 'create', 'configmap', 'iap-config',
        '--from-literal=iap.audience=/projects/{}/global/backendServices/{}'.format(
            project_number,
            backend_service_id
        )
    ])


def __helpers_config(simulation):
    """ setup helper variables """
    helpers.START_TIME = datetime.utcnow().strftime('%Y%m%d%H%M')
    helpers.DRY_RUN = simulation
    helpers.BASE_DIR = os.path.join(os.path.dirname(
        os.path.abspath(inspect.stack()[0][1])), '..')


if __name__ == '__main__':
    __run_steps() # pylint: disable=no-value-for-parameter
