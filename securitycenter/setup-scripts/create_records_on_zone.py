#!/usr/bin/env python3

import argparse

import helpers
from parser_arguments import add_simulation_arguments
from gcp_utils.dns import validate_project_access, create_new_dns_record

def create_parser():
    """CLI parser"""
    parser=argparse.ArgumentParser(description='Create DNS zone and get nameservers')

    parser.add_argument('-dz',
                        '--dns_zone',
                        help='The id of the DNS zone.',
                        dest='dns_zone_name',
                        required=True)

    parser.add_argument('-d',
                        '--dns_project_id',
                        help='The DNS Project id.',
                        dest='dns_project_id',
                        required=True)

    parser.add_argument('-n',
                        '--record_name',
                        help='The name of record to be add',
                        dest='record_name',
                        required=True)
    
    parser.add_argument('-ttl',
                        '--ttl',
                        help='The ttl of record to be add',
                        dest='ttl',
                        required=True)

    parser.add_argument('-v',
                        '--value',
                        help='The value of record to be add',
                        dest='record_value',
                        required=True)

    parser.add_argument('-t',
                        '--record_type',
                        help='The type of record to be add',
                        dest='record_type',
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
    create_new_dns_record(args.dns_project_id,
                          args.dns_zone_name,
                          args.record_type,
                          args.record_name,
                          args.ttl,
                          args.record_value)
