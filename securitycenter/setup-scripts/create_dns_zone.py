#!/usr/bin/env python3

import argparse

import helpers
from parser_arguments import add_simulation_arguments
from gcp_utils.dns import validate_project_access, create_dns_zone

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
    create_dns_zone(args.custom_domain, args.dns_zone, args.dns_project_id)
