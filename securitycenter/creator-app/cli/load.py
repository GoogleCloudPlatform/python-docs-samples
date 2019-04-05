#!/usr/bin/env python

"""Load configurations."""

import argparse
import json
import logging
import os

import jsonpickle
import yaml
import sys

from google.cloud import pubsub

from ds_helpers import (list_all_from_kind, delete_record, delete_all_from_kind, add_records)
from validations import (
    validate_yaml,
    validate_mode_values,
    print_validation_failure,
    print_notice
)


STATUS_TOPIC = "publish_status"
RUN_QUERY_TOPIC = "demomode"


def run_load_py():
    parser = argparse.ArgumentParser(
        description='Load configuration utilities',
        add_help=False)

    parser.add_argument(
        '-h', '--help',
        help='Display the command help',
        action='store_true')

    parser.add_argument(
        'command',
        choices=['execute_queries', 'event_queries', 'delete_all_queries', 'delete_query', 'list_queries', 'mode'],
        help='Load a command',
        nargs='?')

    args, sub_args = parser.parse_known_args()
    execute_command(args, parser, sub_args)


def execute_queries(project):
    data = '{{}}'.encode('utf-8')
    publish(data, project, RUN_QUERY_TOPIC)


def execute_command(args, parser, sub_args):
    if args.help:
        if args.command is None:
            logging.debug(parser.print_help())
            sys.exit(1)
        sub_args.append('--help')
    elif args.command == 'execute_queries':
        execute_command_execute_queries(parser, sub_args)
    elif args.command == 'event_queries':
        execute_command_event_query(sub_args)
    elif args.command == 'list_queries':
        execute_command_list_query()
    elif args.command == 'delete_all_queries':
        execute_command_delete_all_queries()
    elif args.command == 'delete_query':
        execute_command_delete_query(sub_args)
    elif args.command == 'mode':
        execute_command_mode(sub_args)
    else:
        parser.error('Command not found')


def execute_command_execute_queries(parser, sub_args):
    add_project_arg(parser)
    command_args = parser.parse_args(sub_args)
    execute_queries(command_args.project)
    print_notice('Queries execution called.')


def execute_command_event_query(sub_args):
    parser = argparse.ArgumentParser(description='Load rules configuration')
    parser.add_argument(
        '-f',
        '--yaml_file',
        help='Path to a YAML file with the rules to be loaded',
        required=True
    )
    add_project_arg(parser)
    command_args = parser.parse_args(sub_args)
    load_query(command_args.yaml_file)
    print_notice('Event Query list loaded.')


def execute_command_list_query():
    queries = list_all_from_kind()
    print_notice('--- Queries List Start ---')
    for query in queries:
        print('QUERY_NAME:{}, QUERY_ID:{}'.format(query['name'], query.key.id_or_name))
    print_notice('--- Queries List End ---')


def execute_command_delete_all_queries():
    delete_all_from_kind()
    delete_all_from_kind(kind='EventQueryExecution')
    print_notice('--- All queries deleted ---')


def execute_command_delete_query(sub_args):
    parser = argparse.ArgumentParser(description='Delete query by key')
    parser.add_argument(
        '-k',
        '--key',
        dest='ds_key',
        help='Key of the query on DataStore to be deleted',
        required=True
    )
    add_project_arg(parser)
    command_args = parser.parse_args(sub_args)
    ds_key = int(command_args.ds_key)
    delete_record(ds_key)
    delete_record(ds_key, kind='EventQueryExecution')
    print_notice('Query with key:{} deleted.'.format(ds_key))


def execute_command_mode(sub_args):
    parser = argparse.ArgumentParser(
        description='Load rules configuration')
    parser.add_argument(
        '-m',
        '--mode',
        metavar='PRODUCTION|DEMO',
        help='Creator App processing status mode',
        required=True)
    add_project_arg(parser)
    command_args = parser.parse_args(sub_args)
    validate_mode_values(command_args.mode)
    set_processing_status(command_args.project, command_args.mode)
    print_notice('Processing status set.')


def load_query(yaml_file):
    if not os.path.isfile(yaml_file):
        print("load.py: error: event query yaml file not found: \"{}\". ".format(yaml_file))
        sys.exit(3)

    stream = load_yaml_file(yaml_file)
    validate_yaml(stream)
    json_queries = convert_to_json(stream)
    data = json_queries.encode('utf-8')
    payload = json.loads(data.decode('utf-8'))
    properties_array = ['joins', 'steps', 'name', 'threshold', 'topic']
    add_records(payload, properties_array)


def load_yaml_file(yaml_file):
    try:
        with open(yaml_file, 'r') as myfile:
            data = myfile.read()
            stream = yaml.load(data)
        return stream
    except Exception as ex:
        print_validation_failure(
            'File {} is not a valid YAML file'
            .format(yaml_file))
        print_validation_failure(ex)
        sys.exit(4)


def set_processing_status(project, mode):
    data = '{{"status": "{}"}}'.format(mode).encode('utf-8')
    publish(data, project, STATUS_TOPIC)


def add_project_arg(parser):
    parser.add_argument(
        '-p',
        '--project',
        help='The Creator project id',
        dest='project',
        required=True
    )


def convert_to_json(stream):
    return jsonpickle.encode(stream, unpicklable=False)


def publish(data, project, topic):
    publisher = pubsub.PublisherClient()
    topic_path = publisher.topic_path(project, topic)
    attributes_dict = {}
    publisher.publish(topic_path, data, **attributes_dict)


if __name__ == '__main__':
    from colorama import init
    init()
    run_load_py()
