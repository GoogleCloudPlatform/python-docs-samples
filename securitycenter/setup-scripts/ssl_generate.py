#!/usr/bin/env python3

import io
import os
import sys

import argparse
from gcp_utils.addresses import external_ip, get_external_ip
from gcp_utils.dns import dns_records
from gcp_utils.firewall import firewall_rules
from gcp_utils.machine import gce_machine
from gcp_utils.projects import has_access_to_project

import helpers
from base import LOGGER, log_exception, run_command, green_print
from parser_arguments import add_simulation_arguments


def create_parser():
    """CLI parser"""
    parser = argparse.ArgumentParser(description='Create DNS zone and get nameservers')

    parser.add_argument(
        '-md',
        '--main_domain',
        help='Main domain',
        dest='main_domain',
        required=True)

    parser.add_argument(
        '-dz',
        '--dns_zone',
        help='The id of the DNS zone.',
        dest='dns_zone',
        required=True)

    parser.add_argument(
        '-d',
        '--dns_project_id',
        help='The id of the dns project',
        dest='dns_project_id',
        required=True)

    parser.add_argument(
        '-e',
        '--email',
        help='The user email that will receive notifications about the ssl certificate expiration',
        dest='email',
        required=True)

    parser.add_argument(
        '-psd',
        '--prefix_sub_domains',
        help='The sub-domains prefixes separated by ","',
        dest='prefix_sub_domains',
        required=False)

    parser.add_argument(
        '--debug',
        '--DEBUG',
        help='Prints all outputs from commands.',
        dest='debug',
        action='store_true')

    parser.set_defaults(dry_run=True)
    parser.set_defaults(debug=False)

    return parser


def generate_certs_file(main_domain,
                        user_email,
                        compute_zone,
                        dns_project_id,
                        prefix_sub_domains):

    filename = create_docker_file(main_domain,
                                  user_email,
                                  prefix_sub_domains)
    execute_docker_file_remotely(filename, dns_project_id, compute_zone)
    drop_docker_file(filename)


def execute_docker_file_remotely(filename, dns_project_id, compute_zone):
    with log_exception():
        LOGGER.info("Sending docker_creation_file to docker")
        cmd = [
            "gcloud", "compute", "scp",
            "--project", dns_project_id,
            "--zone", compute_zone,
            "docker_creation_file.sh",
            "ssl-certificate-gen:{}".format(filename)
        ]
        run_command(cmd)
        LOGGER.info("Executing file")
        cmd = [
            "gcloud", "compute", "ssh", '"ssl-certificate-gen"',
            "--project", dns_project_id,
            "--zone", compute_zone,
            "--command", "'. docker_creation_file.sh'"
        ]
        run_command(cmd)


def download_certs_file(dns_project_id, compute_zone, main_domain):
    with log_exception():
        path = os.getcwd()
        cmd = [
            "gcloud", "compute", "scp",
            "--project", dns_project_id,
            "--zone", compute_zone,
            "ssl-certificate-gen:~/certs.zip",
            "certs-{}.zip".format(main_domain)
        ]
        run_command(cmd)
        return "Your file is in: {}/certs-{}.zip".format(path, main_domain)


def drop_docker_file(filename):
    try:
        LOGGER.info("Removing docker file")
        os.remove(filename)
    except OSError:
        pass


def create_docker_file(main_domain, user_email, prefix_sub_domains):
    filename = "docker_creation_file.sh"
    with io.FileIO(filename, "w") as file:
        file.write(str.encode(file_set_env(main_domain, user_email) + "\n"))
        file.write(str.encode(file_create_docker_volume() + "\n"))
        if prefix_sub_domains:
            for prefix in prefix_sub_domains:
                file.write(str.encode(
                    file_create_certificates(
                        main_domain,
                        user_email,
                        prefix) + "\n"))
        else:
            file.write(str.encode(
                file_create_certificates(
                    main_domain,
                    user_email, "") + "\n"))
        file.write(str.encode(file_get_location_volume() + "\n"))
        file.write(str.encode(file_copy_localy() + "\n"))
        file.write(str.encode(file_change_owner() + "\n"))
        file.write(str.encode(file_rename_directory(prefix_sub_domains) + "\n"))
        file.write(str.encode(file_create_zip_file() + "\n"))
    file.close()
    return filename


def log_ssl_certificate_machine(compute_zone, dns_project_id):
    LOGGER.info("Logging ssl certificate machine")
    cmd = [
        'gcloud', 'compute', 'ssh',
        '--zone', compute_zone,
        '--project', dns_project_id,
        'ssl-certificate-gen'
    ]
    run_command(cmd)


def file_set_env(main_domain, user_email):
    return "yourdomain={};youremail={}".format(main_domain, user_email)


def file_create_docker_volume():
    cmd = [
        "docker", "volume", "create", "--name", "nginx-certs"
    ]
    return " ".join(cmd)


def file_create_certificates(your_domain, your_email, prefix_domain):
    domain = your_domain
    if prefix_domain:
        domain = "{}.{}".format(prefix_domain, your_domain)

    cmd = [
        "docker", "run",
        "-v", "nginx-certs:/etc/letsencrypt",
        "-e", "http_proxy=$http_proxy",
        "-e", "domains={}".format(domain),
        "-e", "email={}".format(your_email),
        "-p", "80:80 -p 443:443",
        "--rm", "pierreprinetti/certbot:latest"
    ]
    return " ".join(cmd)


def file_get_location_volume():
    cmd = [
        "export", "docker_volume_location=$({})"
        .format("docker volume inspect nginx-certs --format '{{ .Mountpoint }}'")
    ]
    return " ".join(cmd)


def file_copy_localy():
    cmd = [
        "sudo", "cp", "-r", " ${docker_volume_location}/archive certs"
    ]
    return " ".join(cmd)


def file_change_owner():
    cmd = [
        "sudo", "chown", "-R", "$USER:$USER certs/"
    ]
    return " ".join(cmd)


def file_create_zip_file():
    cmd = [
        "docker",
        "run",
        "-v", "$(pwd):/to_zip",
        "-w", "/to_zip",
        "-u", "$(id -u):$(id -g)",
        "brandography/alpine-zip",
        "zip", "-r9",
        "certs.zip", "certs"
    ]
    return " ".join(cmd)


def file_rename_directory(prefix_sub_domains):
    commands = ""
    for prefix in prefix_sub_domains:
        domain = "{}.".format(prefix)
        domain = domain+"${yourdomain}"
        cmd = [
            "(", "cd", "certs;",
            "mv", "{}".format(domain),
            "{};)".format(prefix)
        ]
        commands += " ".join(cmd) + "\n"
    return commands


def format_sub_domains(main_domain, prefix_sub_domains):
    sub_domains = []
    if prefix_sub_domains:
        for sub_domain in  prefix_sub_domains.split(","):
            sub_domains.append("{}.{}".format(sub_domain.strip(),
                                              main_domain.strip())
                              )
    return sub_domains

def validate_arguments(args):
    if not has_access_to_project(args.dns_project_id):
        print(('Project {} not found. '
               'Please check '
               'if project id is correct and '
               'if you have been granted access to it.'
               .format(args.dns_project_id)))
        sys.exit(1)


def execute_steps(args):
    validate_arguments(args)
    compute_zone = "us-central1-a"
    compute_region = "us-central1"
    external_ip_name = "ssl-external-ip"

    sub_domains = format_sub_domains(args.main_domain, args.prefix_sub_domains)

    domains = sub_domains if sub_domains else [args.main_domain]

    with external_ip(args.dns_project_id, compute_region, external_ip_name):
        if not helpers.DRY_RUN:
            ssl_external_ip = get_external_ip(args.dns_project_id, external_ip_name)
        else:
            ssl_external_ip = "172.168.32.12"

        with firewall_rules(
            args.dns_project_id, [
                 {
                  "port": 443,
                  "tag": "https-server",
                  "name": "ssl-certificate-gen-allow-https-for-tag"
                },
                {
                  "port": 80,
                  "tag": "http-server",
                  "name": "ssl-certificate-gen-allow-http-for-tag"
                }
            ]):

            records_name = domains
            records = {}
            for record_name in records_name:
                records[record_name] = {}
                records[record_name]['ttl'] = "90"
                records[record_name]['type'] = "A"
                records[record_name]['value'] = ssl_external_ip

            with dns_records(args.dns_project_id,
                             args.dns_zone,
                             records):

                with gce_machine(args.dns_project_id,
                                 compute_zone,
                                 ssl_external_ip):

                    sub_domains = (args.prefix_sub_domains.split(",")
                                   if args.prefix_sub_domains else [])

                    generate_certs_file(args.main_domain,
                                        args.email,
                                        compute_zone,
                                        args.dns_project_id,
                                        sub_domains)

                    certs_path = download_certs_file(args.dns_project_id,
                                                     compute_zone,
                                                     args.main_domain)

    green_print(certs_path)


if __name__ == '__main__':
    LOGGER.info("Starting process!")
    parser = create_parser()
    add_simulation_arguments(parser)
    args = parser.parse_args()
    helpers.DRY_RUN = args.dry_run
    helpers.DEBUG = args.debug
    execute_steps(args)
    LOGGER.info("Finished!")
