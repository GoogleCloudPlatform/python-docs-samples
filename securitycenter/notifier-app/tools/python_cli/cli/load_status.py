"""Load status."""
import logging

from python_cli import api_client
from python_cli.api_client.rest import ApiException
from python_cli.cli.cli_utils import setup_api_instance


def load_status(status, gcpid, token, api_endpoints_url):
    """Load status."""
    call_api(status, token, api_endpoints_url)
    logging.debug("Execution status is %s ", status)


def call_api(status, token, api_endpoints_url):
    """Call Endpoints API."""
    api_instance = setup_api_instance(api_client, api_endpoints_url, token)
    body = api_client.StatusRequest()
    body.status = status

    try:
        api_instance.gcp_noti_api_set_status_with_http_info(body=body)
    except ApiException as ex:
        logging.warn(("Exception when calling "
                      "DefaultApi->"
                      "gcp_noti_api_set_status_with_http_info: %s\n"), ex)
