"""Load the channels configuration from an YAML file."""
from __future__ import print_function

import logging

import os
import os.path

import sys
import yaml

import api_client
from python_cli.api_client.rest import ApiException
from python_cli.cli.cli_utils import read_file, setup_api_instance


def load_channels_config(config, gcpid, access_token, api_endpoints_url):
    """Load the channels configuration."""
    if os.path.isfile(config):
        content = read_file(config)
        stream = yaml.load(content)
        configuration = from_yaml_to_dict(stream)
        call_api(configuration, access_token, api_endpoints_url)
    else:
        logging.warn('No Configuration file %s is to a valid file.', config)
        sys.exit(1)

    logging.debug(("Channel configuration file: %s\n"
                   "GCP id: %s "), config, gcpid)


def from_yaml_to_dict(content):
    """Transform configuration from YAML to dict."""
    api_config = {}
    configs = content['configuration']
    for conf in configs:
        item = conf['item']
        for prop in conf['properties']:
            for key, value in prop.items():
                api_config[item + "_" + key] = value
    return api_config


def call_api(configuration, token, api_endpoint_url):
    """Call Endpoints API."""
    api_instance = setup_api_instance(api_client, api_endpoint_url, token)
    body = api_client.ConfigurationRequestBody()
    body.configuration = configuration
    try:
        api_instance.gcp_noti_api_config_with_http_info(body=body)
    except ApiException as ex:
        logging.warn(("Exception when calling "
                      "DefaultApi->"
                      "gcp_noti_api_config_with_http_info: %s\n"), ex)
