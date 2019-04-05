#!/usr/bin/env python3

import argparse

import helpers
from parser_arguments import add_simulation_arguments
from gcp_utils.dns import delegate_zone, validate_project_access

def create_parser():
    """CLI parser"""
    parser=argparse.ArgumentParser(description='Create DNS zone and get nameservers')

    parser.add_argument('-c',
                        '--custom_domain',
                        help='The custom domain to be configured.',
                        dest='custom_domain',
                        required=True)

    parser.add_argument('-rdz',
                        '--root_dns_zone',
                        help='The id of the root DNS zone.',
                        dest='root_dns_zone_name',
                        required=True)

    parser.add_argument('-rd',
                        '--root_dns_project_id',
                        help='The root DNS Project id.',
                        dest='root_dns_project_id',
                        required=True)

    parser.add_argument('-ddz',
                        '--delegate_dns_zone',
                        help='The the NS zone id that will receive delegation',
                        dest='delegate_dns_zone_name',
                        required=True)

    parser.add_argument('-dd',
                        '--delegate_dns_project_id',
                        help='The DNS Project id that will receive delegation.',
                        dest='delegate_dns_project_id',
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
    validate_project_access(args.root_dns_project_id, 1)
    validate_project_access(args.delegate_dns_project_id, 1)


if __name__ == '__main__':
    parser = create_parser()
    add_simulation_arguments(parser)
    args = parser.parse_args()
    validate_arguments(args)
    helpers.DRY_RUN = args.dry_run
    helpers.DEBUG = args.debug
    delegate_zone(args.root_dns_project_id,
                  args.root_dns_zone_name,
                  args.delegate_dns_project_id,
                  args.delegate_dns_zone_name,
                  args.custom_domain)
