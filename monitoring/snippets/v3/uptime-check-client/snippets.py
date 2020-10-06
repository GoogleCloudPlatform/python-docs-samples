# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import argparse
import os
import pprint

from google.cloud import monitoring_v3
from google.protobuf import field_mask_pb2
import tabulate


# [START monitoring_uptime_check_create]
def create_uptime_check_config_get(project_name, host_name=None, display_name=None):
    config = monitoring_v3.UptimeCheckConfig()
    config.display_name = display_name or "New GET uptime check"
    config.monitored_resource = {
        "type": "uptime_url",
        "labels": {"host": host_name or "example.com"}
    }
    config.http_check = {
        "request_method": monitoring_v3.UptimeCheckConfig.HttpCheck.RequestMethod.GET,
        "path": "/",
        "port": 80
    }
    config.timeout = {"seconds": 10}
    config.period = {"seconds": 300}

    client = monitoring_v3.UptimeCheckServiceClient()
    new_config = client.create_uptime_check_config(request={"parent": project_name, "uptime_check_config": config})
    pprint.pprint(new_config)
    return new_config


def create_uptime_check_config_post(project_name, host_name=None, display_name=None):
    config = monitoring_v3.UptimeCheckConfig()
    config.display_name = display_name or "New POST uptime check"
    config.monitored_resource = {
        "type": "uptime_url",
        "labels": {"host": host_name or "example.com"}
    }
    config.http_check = {
        "request_method": monitoring_v3.UptimeCheckConfig.HttpCheck.RequestMethod.POST,
        "content_type": monitoring_v3.UptimeCheckConfig.HttpCheck.ContentType.URL_ENCODED,
        "body": "foo=bar".encode("utf-8"),
        "path": "/",
        "port": 80
    }
    config.timeout = {"seconds": 10}
    config.period = {"seconds": 300}

    client = monitoring_v3.UptimeCheckServiceClient()
    new_config = client.create_uptime_check_config(request={"parent": project_name, "uptime_check_config": config})
    pprint.pprint(new_config)
    return new_config


# [END monitoring_uptime_check_create]

# [START monitoring_uptime_check_update]
def update_uptime_check_config(
    config_name, new_display_name=None, new_http_check_path=None
):
    client = monitoring_v3.UptimeCheckServiceClient()
    config = client.get_uptime_check_config(request={"name": config_name})
    field_mask = field_mask_pb2.FieldMask()
    if new_display_name:
        field_mask.paths.append("display_name")
        config.display_name = new_display_name
    if new_http_check_path:
        field_mask.paths.append("http_check.path")
        config.http_check.path = new_http_check_path
    client.update_uptime_check_config(request={"uptime_check_config": config, "update_mask": field_mask})


# [END monitoring_uptime_check_update]


# [START monitoring_uptime_check_list_configs]
def list_uptime_check_configs(project_name):
    client = monitoring_v3.UptimeCheckServiceClient()
    configs = client.list_uptime_check_configs(request={"parent": project_name})

    for config in configs:
        pprint.pprint(config)


# [END monitoring_uptime_check_list_configs]


# [START monitoring_uptime_check_list_ips]
def list_uptime_check_ips():
    client = monitoring_v3.UptimeCheckServiceClient()
    ips = client.list_uptime_check_ips(request={})
    print(
        tabulate.tabulate(
            [(ip.region, ip.location, ip.ip_address) for ip in ips],
            ("region", "location", "ip_address"),
        )
    )


# [END monitoring_uptime_check_list_ips]


# [START monitoring_uptime_check_get]
def get_uptime_check_config(config_name):
    client = monitoring_v3.UptimeCheckServiceClient()
    config = client.get_uptime_check_config(request={"name": config_name})
    pprint.pprint(config)


# [END monitoring_uptime_check_get]


# [START monitoring_uptime_check_delete]
# `config_name` is the `name` field of an UptimeCheckConfig.
# See https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.uptimeCheckConfigs#UptimeCheckConfig.
def delete_uptime_check_config(config_name):
    client = monitoring_v3.UptimeCheckServiceClient()
    client.delete_uptime_check_config(request={"name": config_name})
    print("Deleted ", config_name)


# [END monitoring_uptime_check_delete]


class MissingProjectIdError(Exception):
    pass


def project_id():
    """Retreieves the project id from the environment variable.

    Raises:
        MissingProjectIdError -- When not set.

    Returns:
        str -- the project name
    """
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]

    if not project_id:
        raise MissingProjectIdError(
            "Set the environment variable "
            + "GCLOUD_PROJECT to your Google Cloud Project Id."
        )
    return project_id


def project_name():
    return "projects/" + project_id()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Demonstrates Uptime Check API operations."
    )

    subparsers = parser.add_subparsers(dest="command")

    list_uptime_check_configs_parser = subparsers.add_parser(
        "list-uptime-check-configs", help=list_uptime_check_configs.__doc__
    )

    list_uptime_check_ips_parser = subparsers.add_parser(
        "list-uptime-check-ips", help=list_uptime_check_ips.__doc__
    )

    create_uptime_check_config_get_parser = subparsers.add_parser(
        "create-uptime-check-get", help=create_uptime_check_config_get.__doc__
    )
    create_uptime_check_config_get_parser.add_argument(
        "-d", "--display_name", required=False,
    )
    create_uptime_check_config_get_parser.add_argument(
        "-o", "--host_name", required=False,
    )

    create_uptime_check_config_post_parser = subparsers.add_parser(
        "create-uptime-check-post", help=create_uptime_check_config_post.__doc__
    )
    create_uptime_check_config_post_parser.add_argument(
        "-d", "--display_name", required=False,
    )
    create_uptime_check_config_post_parser.add_argument(
        "-o", "--host_name", required=False,
    )

    get_uptime_check_config_parser = subparsers.add_parser(
        "get-uptime-check-config", help=get_uptime_check_config.__doc__
    )
    get_uptime_check_config_parser.add_argument(
        "-m", "--name", required=True,
    )

    delete_uptime_check_config_parser = subparsers.add_parser(
        "delete-uptime-check-config", help=delete_uptime_check_config.__doc__
    )
    delete_uptime_check_config_parser.add_argument(
        "-m", "--name", required=True,
    )

    update_uptime_check_config_parser = subparsers.add_parser(
        "update-uptime-check-config", help=update_uptime_check_config.__doc__
    )
    update_uptime_check_config_parser.add_argument(
        "-m", "--name", required=True,
    )
    update_uptime_check_config_parser.add_argument(
        "-d", "--display_name", required=False,
    )
    update_uptime_check_config_parser.add_argument(
        "-p", "--uptime_check_path", required=False,
    )

    args = parser.parse_args()

    if args.command == "list-uptime-check-configs":
        list_uptime_check_configs(project_name())

    elif args.command == "list-uptime-check-ips":
        list_uptime_check_ips()

    elif args.command == "create-uptime-check-get":
        create_uptime_check_config_get(
            project_name(), args.host_name, args.display_name
        )
    elif args.command == "create-uptime-check-post":
        create_uptime_check_config_post(
            project_name(), args.host_name, args.display_name
        )

    elif args.command == "get-uptime-check-config":
        get_uptime_check_config(args.name)

    elif args.command == "delete-uptime-check-config":
        delete_uptime_check_config(args.name)

    elif args.command == "update-uptime-check-config":
        if not args.display_name and not args.uptime_check_path:
            print("Nothing to update.  Pass --display_name or " "--uptime_check_path.")
        else:
            update_uptime_check_config(
                args.name, args.display_name, args.uptime_check_path
            )
