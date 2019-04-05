"""Load users."""
from __future__ import print_function

import os
import os.path
import logging

import api_client
from api_client.rest import ApiException

from python_cli.cli.cli_utils import read_file, setup_api_instance


def load_users(userfile, searched_role, gcpid, token, api_endpoints_url):
    """Load users."""
    logging.debug(("userfile: %s,\n"
                   "searched_role: %s,\n"
                   "gcpid: %s,\n"
                   "token: %s,\n"
                   "api_endpoints_url: %s"),
                  userfile, searched_role, gcpid, token, api_endpoints_url)

    if os.path.isfile(userfile):
        content = read_file(userfile)
        users = filter_contents(content, searched_role)
        call_api(users, token, api_endpoints_url)

    else:
        logging.debug('File: %s do not exist', userfile)


def call_api(users, token, api_endpoints_url):
    """Call Endpoints API."""
    api_instance = setup_api_instance(api_client, api_endpoints_url, token)
    body = api_client.UsersRequestBody()
    body.users = users
    try:
        api_instance.gcp_noti_api_users_with_http_info(body=body)
    except ApiException as ex:
        logging.warn(("Exception when calling"
                      "DefaultApi->gcp_noti_api_users_with_http_info: %s\n"),
                     ex)


def filter_contents(content, searched_role):
    """Filter content."""
    search_it = searched_role and len(searched_role) > 0
    users = []
    for line in content.split("\n"):
        line_splitted = line.split(",")
        if len(line_splitted) == 4:
            user = api_client.ApiUser(
                email=line_splitted[0],
                telephone_number=line_splitted[1],
                jira_uid=line_splitted[2],
                role=line_splitted[3].strip('\r')
            )

            if search_it and str(user.role) != searched_role:
                continue

            users.append(user)

    return users
