"""Load active channels."""
from __future__ import print_function

import logging

import api_client
from api_client.rest import ApiException

from python_cli.cli.cli_utils import setup_api_instance


def load_channels(channels, gcpid, token, api_endpoints_url):
    """Load active channels."""
    logging.debug(("channels: %s,\n"
                   "gcpid: %s,\n"
                   "token: %s,\n"
                   "api_endpoints_url: %s"),
                  channels, gcpid, token, api_endpoints_url)

    api_channels = []

    for channel in channels[0].upper().replace("'", "").split(","):
        api_channels.append(api_client.ChannelRequest(channel.strip()))

    call_api(api_channels, token, api_endpoints_url)


def call_api(channels, token, api_endpoints_url):
    """Call Endpoints API."""
    api_instance = setup_api_instance(api_client, api_endpoints_url, token)
    body = api_client.ChannelsRequestBody()
    body.active_channels = channels
    try:
        api_instance.gcp_noti_api_channels_with_http_info(body=body)
    except ApiException as ex:
        logging.warn(("Exception when calling "
                      "DefaultApi->gcp_noti_api_channels_with_http_info: %s\n"),
                     ex)
