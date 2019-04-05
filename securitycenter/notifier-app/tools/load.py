#!/usr/bin/env python

"""Load configurations."""

import argparse
import logging
import sys

from python_cli.cli.load_channels import load_channels
from python_cli.cli.load_channels_config import load_channels_config
from python_cli.cli.load_extra_info import load_extra_info
from python_cli.cli.load_rules import load_rules
from python_cli.cli.load_status import load_status
from python_cli.cli.load_users import load_users


def add_default_args():
    """Add default arguments to CLI parser."""
    parser.add_argument(
        '-e', '--api_endpoints_url', help='API Endpoint URL ending in _ah/api',
        required=True)
    parser.add_argument(
        '-a', '--access_token', help='API KEY (required)',
        required=True)
    parser.add_argument(
        '-g', '--gcpid', help='GCP project ID (required)', required=True)


parser = argparse.ArgumentParser(
    description='Load configuration utilities',
    add_help=False)

parser.add_argument(
    'command',
    choices=['users',
             'extra_info',
             'channels',
             'config',
             'rules',
             'start',
             'stop'],
    help='Load a command',
    nargs='?')

parser.add_argument(
    '-h', '--help',
    help='Display the command help',
    action='store_true')

if not len(sys.argv) > 1:
    parser.print_help()
    sys.exit(1)

args, sub_args = parser.parse_known_args()

if args.help:
    if args.command is None:
        logging.debug(parser.print_help())
        sys.exit(1)

    sub_args.append('--help')

if args.command == 'users':
    parser = argparse.ArgumentParser(
        description='Adds users to be notified by the application')

    parser.add_argument(
        '-f', '--userfile', help='Path to user file (required)',
        required=True)

    parser.add_argument(
        '-filt', '--filter', nargs='?', help='Filter users by role')

    add_default_args()

    commandArgs = parser.parse_args(sub_args)

    load_users(commandArgs.userfile,
               commandArgs.filter,
               commandArgs.gcpid,
               commandArgs.access_token,
               commandArgs.api_endpoints_url)

elif args.command == 'extra_info':
    parser = argparse.ArgumentParser(
        description='Adds an extra info to the notification')

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        '-m', '--message', help='Message to be added to the notification')

    group.add_argument(
        '-f', '--file',
        help='Path to a file with a text to be added to the notification')

    parser.add_argument('-n', '--notitype',
                        help='Notification type',
                        required=True)

    add_default_args()

    commandArgs = parser.parse_args(sub_args)
    load_extra_info(
        commandArgs.message,
        commandArgs.file,
        commandArgs.notitype,
        commandArgs.gcpid,
        commandArgs.access_token,
        commandArgs.api_endpoints_url)

elif args.command == 'channels':
    parser = argparse.ArgumentParser(description='Load active channels')

    parser.add_argument(
        '-c', '--channel',
        nargs=1, help='Active channels (required)', required=True)

    add_default_args()

    commandArgs = parser.parse_args(sub_args)
    load_channels(commandArgs.channel,
                  commandArgs.gcpid,
                  commandArgs.access_token,
                  commandArgs.api_endpoints_url)

elif args.command == 'config':
    parser = argparse.ArgumentParser(
        description='Load configuration')

    parser.add_argument(
        '-c', '--config',
        help='configuration (required)', required=True)

    add_default_args()

    commandArgs = parser.parse_args(sub_args)
    load_channels_config(commandArgs.config,
                         commandArgs.gcpid,
                         commandArgs.access_token,
                         commandArgs.api_endpoints_url)
elif args.command == 'start':
    add_default_args()
    commandArgs = parser.parse_args(sub_args)
    load_status('START',
                commandArgs.gcpid,
                commandArgs.access_token,
                commandArgs.api_endpoints_url)
elif args.command == 'stop':
    add_default_args()
    commandArgs = parser.parse_args(sub_args)
    load_status('STOP',
                commandArgs.gcpid,
                commandArgs.access_token,
                commandArgs.api_endpoints_url)
elif args.command == 'rules':
    parser = argparse.ArgumentParser(
        description='Load rules configuration')

    parser.add_argument(
        '-f', '--yaml_file',
        help='Path to a YAML file with the rules to be loaded', required=True)

    add_default_args()

    commandArgs = parser.parse_args(sub_args)
    load_rules(
        commandArgs.yaml_file,
        commandArgs.gcpid,
        commandArgs.access_token,
        commandArgs.api_endpoints_url)
else:
    parser.error('Command not found')
