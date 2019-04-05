#!/usr/bin/env python3
"""
Script that creates a sample file
to be used as input on run_setup of query_builder
"""
import inspect
import json
import os
import time
from collections import namedtuple
from contextlib import contextmanager
from datetime import datetime

import click
import timeout_decorator
from colorama import init

import helpers
from base import LOGGER
from compute_handler import get_backend_service_id
from kubernetes_handler import (
    delete_configmap,
    get_cluster_credentials,
    patch_deployment)
from setup_iap import setup_iap
from simulation_mode import simulation_wall

init()


@click.command()
@click.option('--input-file',
              help='Input file', required=True)
@click.option('--simulation/--no-simulation',
              default=True,
              help='Simulate the execution. Do not execute any command.')
def run_query_builder_iap_setup(simulation, input_file):
    """ run query builder setup """
    with simulation_wall(simulation):
        try:
            query_builder_input = parse_input_json(input_file)
            helpers_config(simulation)
            click.echo("Input file read from [{}]".format(input_file))
        except FileNotFoundError as not_found:
            click.echo("File [{0}] not found.".format(not_found.filename))
        except json.decoder.JSONDecodeError as err:
            click.echo("Error parsing file [{0}].\n{1}"
                       .format(input_file, err))
        with instruction_separator("Cluster Credentials"):
            get_cluster_credentials(
                query_builder_input.query_builder.project_id,
                query_builder_input.cluster.cluster_name,
                query_builder_input.query_builder.compute_zone
            )

        check_load_balancer(query_builder_input)

        with instruction_separator("IAP", "Turning on"):
            delete_configmap("iap-config")

            setup_iap(query_builder_input.query_builder.project_id,
                      query_builder_input.oauth.client_id,
                      query_builder_input.oauth.client_secret,
                      query_builder_input.cluster.timeout)

        with instruction_separator("Frontend Deployment", "Patching"):
            frontend_deployment = "frontend"
            path_value = '"{\\"spec\\":{\\"template\\":{\\"metadata\\":{\\"annotations\\":{\\"date\\":\\"'+ datetime.utcnow().strftime('%Y%m%d%H%M%S') + '\\"}}}}}"'
            patch_deployment(frontend_deployment, path_value)


@contextmanager
def instruction_separator(step, action="Creating"):
    """Add a message at the start and end of the log messages of the step"""
    click.echo()
    click.secho('{:-^60}'.format(("{} {}".format(action, step))), bold=True)
    try:
        yield
        click.secho('{:-^60}'.format(("{} finished successfully".format(step))),
                    fg='green')
    except StopIteration as err:
        LOGGER.exception("Timeout error")
        click.secho('{:-^60}'.format(("Timeout {} {}".format(action, step))),
                    err=True, fg='red')
        raise ValueError(str(err))
    except Exception:  # pylint: disable=W0703
        LOGGER.exception("error")
        click.secho('{:-^60}'.format(("Problem {} {}".format(action, step))),
                    err=True, fg='red')


@timeout_decorator.timeout(1800, timeout_exception=StopIteration)
def check_load_balancer(query_builder_input):
    """ """
    with instruction_separator("Load Balancer", "Checking"):
        backend_service = get_backend_service_id(
            query_builder_input.query_builder.project_id,
            "frontend"
        )
        while not backend_service:
            click.echo("Waiting for Load Balancer")
            if backend_service == "":
                time.sleep(60)
            backend_service = get_backend_service_id(
                query_builder_input.query_builder.project_id,
                "frontend"
            )


def parse_input_json(input_file):
    """ Parse input json """
    with open(input_file, 'r', encoding='utf-8') as infile:
        return json.loads(
            infile.read(),
            object_hook=lambda d: namedtuple('QB', d.keys())(*d.values())
        )


def helpers_config(simulation):
    """ setup helper variables """
    helpers.START_TIME = datetime.utcnow().strftime('%Y%m%d%H%M')
    helpers.DRY_RUN = simulation
    helpers.BASE_DIR = os.path.join(os.path.dirname(
        os.path.abspath(inspect.stack()[0][1])))


if __name__ == '__main__':
    run_query_builder_iap_setup()  # pylint: disable=no-value-for-parameter
