"""Load extra info."""
from __future__ import print_function

import logging
import sys


from python_cli import api_client
from python_cli.api_client.rest import ApiException
from python_cli.cli.cli_utils import read_file, setup_api_instance


def load_extra_info(message, userfile, notitype, gcpid, token,
                    api_endpoints_url):
    """Load extra info."""
    if not (message or userfile):
        logging.warn('No message passed, add -message or -file')
        sys.exit(1)

    if userfile:
        extra_info = read_file(userfile)
    else:
        extra_info = message

    call_api(notitype, extra_info, token, api_endpoints_url)

    logging.debug(("Message: %s,\n"
                   "File: %s,\n"
                   "Notification type: %s,\n"
                   "GCP id: %s"),
                  message, userfile, notitype, gcpid)


def call_api(notitype, extra_info, token, api_endpoints_url):
    """Call Endpoints API."""
    api_instance = setup_api_instance(api_client, api_endpoints_url, token)

    body = api_client.ExtraInfoRequestBody()
    body.notification_type = notitype
    body.info = extra_info

    try:
        api_instance.gcp_noti_api_set_extra_info_with_http_info(body=body)
    except ApiException as ex:
        logging.warn(("Exception when calling"
                      "DefaultApi->"
                      "gcp_noti_api_set_extra_info_with_http_info: %s\n"),
                     ex)
