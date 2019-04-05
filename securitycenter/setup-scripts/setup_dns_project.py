#!/usr/bin/env python3

import argparse
import os

import sys

import helpers
from base import run_command, LOGGER
from gcp_utils.projects import has_access_to_project
from parser_arguments import add_simulation_arguments


def create_parser():
    """CLI parser"""
    parser=argparse.ArgumentParser(description='Create DNS zone and get nameservers')

    parser.add_argument('-c',
                        '--custom_domain',
                        help='The custom domain to be configured.',
                        dest='custom_domain',
                        required=True)

    parser.add_argument('-dz',
                        '--dns_zone',
                        help='The id of the DNS zone.',
                        dest='dns_zone',
                        required=True)

    parser.add_argument('-d',
                        '--dns_project_id',
                        help='The DNS Project id.',
                        dest='dns_project_id',
                        required=True)

    parser.add_argument('--debug',
                        '--DEBUG',
                        help='Prints all outputs from commands.',
                        dest='debug',
                        action='store_true')

    parser.set_defaults(dry_run=True)

    return parser


def enable_service_on_project(dns_project_id, service_url):
    LOGGER.info(
        "Enabling {} on project {}".format(service_url, dns_project_id)
    )
    run_command([
        'gcloud', 'services', 'enable', service_url,
        '--project', dns_project_id
    ])


def create_dns_zone(custom_domain, dns_zone, dns_project_id):
    LOGGER.info("Creating DNS Zone {}, on domain {} project {}"
                .format(dns_zone, custom_domain, dns_project_id))

    run_command([
        "gcloud", "dns", "managed-zones", "create",
        '--dns-name="{}."'.format(custom_domain),
        '--description="{} A zone" "{}"'.format(custom_domain, dns_zone),
        "--project", dns_project_id
    ])


def retrieve_servers_names(dns_zone, dns_project_id):
    LOGGER.info("Retrieving names servers in {}, project {}"
                .format(dns_zone, dns_project_id))
    returned_servers = run_command([
        'gcloud', 'dns', 'managed-zones', 'describe', dns_zone,
        '--project', dns_project_id
    ])

    if helpers.DRY_RUN:
        servers = "server1"
    else:
        servers = returned_servers.decode("utf-8")

    LOGGER.warning("Keep these names servers for the next step\n")
    LOGGER.warning(servers)


def validate_project_access(project_id, exit_code):
    if not has_access_to_project(project_id):
        print(('Project {} not found.'
               'Please check if project id is correct '
               'or if you have been granted access to it.'
               .format(project_id)))
        sys.exit(exit_code)


def describe_variables(args):
    print(args)


def validate_arguments(args):
    validate_project_access(args.dns_project_id, 1)


if __name__ == '__main__':
    parser = create_parser()
    add_simulation_arguments(parser)
    args = parser.parse_args()
    validate_arguments(args)
    helpers.DRY_RUN = args.dry_run
    helpers.DEBUG = args.debug
    enable_service_on_project(args.dns_project_id, 'dns.googleapis.com')
    enable_service_on_project(args.dns_project_id, 'compute.googleapis.com')
    enable_service_on_project(args.dns_project_id, 'admin.googleapis.com')
    enable_service_on_project(args.dns_project_id, 'cloudbilling.googleapis.com')
    enable_service_on_project(args.dns_project_id, 'cloudresourcemanager.googleapis.com')
    enable_service_on_project(args.dns_project_id, 'container.googleapis.com')
    enable_service_on_project(args.dns_project_id, 'iam.googleapis.com')
    enable_service_on_project(args.dns_project_id, 'spanner.googleapis.com')
    create_dns_zone(args.custom_domain, args.dns_zone, args.dns_project_id)
    retrieve_servers_names(args.dns_zone, args.dns_project_id)
