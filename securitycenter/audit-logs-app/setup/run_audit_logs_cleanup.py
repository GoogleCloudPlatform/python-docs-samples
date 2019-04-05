#!/usr/bin/env python3
#pylint: disable=missing-docstring, C0301, no-value-for-parameter

import inspect
import json
import os
import re
import sys
from commands import (project_exists, simulation_mode_disclaimer)
from datetime import datetime

import click

import helpers
import logger
from base import run_command, run_command_readonly
from run_setup import __run_commands as __restore_flow
from click_script_commons import configure_helpers


@click.group()
def update_flow():
    pass


@update_flow.command()
@click.option('--project', help='Project', required=True)
@click.option('--simulation/--no-simulation', default=True, help='Simulate the execution. Do not execute any command.')
def cleanup_chain(project, simulation):
    __cleanup_flow(project, simulation)


@update_flow.command()
@click.option('--project', help='Project', required=True)
@click.option('--organization_id', help='organization id', required=True)
@click.option('--cf_bucket', help='Cloud function bucket, this bucket is regional')
@click.option('--df_bucket', help='Dataflow function bucket, this bucket is regional')
@click.option('--bucket_region', help='Cloud function location', required=True)
@click.option('--df_window', help='Dataflow time window, set in minutes')
@click.option('--scc_api_key', help='API Key to access SCC API from your SCC enabled project', required=True)
@click.option('--scc_sa_file', type=click.Path(exists=True), help='Service account for Security Command Center access.', required=True)
@click.option('--org_browser_sa_file', type=click.Path(exists=True), help='Service account for browser access at org level.', required=True)
@click.option('--audit_logs_source_id', help='Source ID to create the findings from', required=True)
@click.option('--simulation/--no-simulation', default=True, help='Simulate the execution. Do not execute any command.')
def restore_chain(organization_id, project, cf_bucket, df_bucket, bucket_region, df_window, scc_api_key, scc_sa_file, org_browser_sa_file, audit_logs_source_id, simulation):
    __restore_flow(organization_id, project, cf_bucket, df_bucket, bucket_region, df_window, scc_api_key, scc_sa_file, org_browser_sa_file, audit_logs_source_id, simulation)


def __get_subscriptions(project):
    cmd = [
        'gcloud', 'pubsub', 'subscriptions', 'list',
        '--project', project, '--format=json'
    ]
    subscriptions = run_command_readonly(cmd).decode("utf-8").strip()
    subscriptions = json.loads(subscriptions)
    return subscriptions


def __delete_subscriptions(project):
    logger.step('Searching and deleting subscriptions')
    subscriptions = __get_subscriptions(project)

    for subscription in subscriptions:
        subscription_name = subscription['name']
        cmd = [
            'gcloud', 'pubsub', 'subscriptions', 'delete',
            subscription_name,
            '--project', project, '--format=json'
        ]
        run_command(cmd)


def __get_functions(project):
    cmd = [
        'gcloud', 'functions', 'list',
        '--project', project, '--format=json'
    ]
    functions = run_command_readonly(cmd).decode("utf-8").strip()
    functions = json.loads(functions)
    return functions


def __delete_functions(project):
    logger.step('Searching and deleting cloud functions')
    functions = __get_functions(project)

    for function in functions:
        function_name = normalized_name(function['name'])
        cmd = [
            'gcloud', 'functions', 'delete', function_name,
            '--project', project, '-q'
        ]
        run_command(cmd)


def normalized_name(full_name):
    if 'functions/' in full_name:
        full_name = full_name.split('functions/')[1]
    return full_name


def __get_dataflow_jobs(project):
    cmd = [
        'gcloud', 'dataflow', 'jobs', 'list',
        '--project', project, '--filter=state=running', '--format=json'
    ]
    jobs = run_command_readonly(cmd).decode("utf-8").strip()
    jobs = json.loads(jobs)
    return jobs


def __cancel_jobs(project):
    logger.step('Searching and deleting Dataflow jobs')
    jobs = __get_dataflow_jobs(project)

    for job in jobs:
        job_id = job['id']
        cmd = [
            'gcloud', 'dataflow', 'jobs', 'cancel', job_id,
            '--project', project
        ]
        run_command(cmd)


def __cleanup_flow(project, simulation):
    # configure helpers
    configure_helpers(simulation)

    # print simulation mode
    simulation_mode_disclaimer()

    # check project
    logger.step('Checking project existence...')
    __validate_project(project)

    # get all subscriptions and delete it
    __delete_subscriptions(project)

    # get all functions and delete it
    __delete_functions(project)

    # get all dataflow jobs and delete it
    __cancel_jobs(project)


def __validate_project(project):
    if not project_exists(project):
        click.echo(('Project {} not found. Please check if id is correct or if '
                    'you have been granted access to it.'.format(project)))
        sys.exit(2)


cli = click.CommandCollection(sources=[update_flow])

if __name__ == '__main__':
    cli()
