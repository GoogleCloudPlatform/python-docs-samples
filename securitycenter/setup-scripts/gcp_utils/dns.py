import sys
from contextlib import contextmanager

import helpers
from .base import LOGGER, run_command, run_command_readonly
from .projects import has_access_to_project


@contextmanager
def dns_transaction(dns_project_id, dns_zone_name):
    try:
        start_transaction(dns_project_id, dns_zone_name)
        yield
        execute_transaction(dns_project_id, dns_zone_name)
    except Exception as err:  # pylint: disable=W0703
        abort_transaction(dns_project_id, dns_zone_name)
        raise err


@contextmanager
def dns_records(dns_project_id, dns_zone_name, records):

    original_records = {}
    original_ttls = {}

    try:
        with dns_transaction(dns_project_id, dns_zone_name):
            for record_name, record in records.items():
                original_record = get_dns_record(dns_project_id,
                                                 dns_zone_name,
                                                 record_name,
                                                 record['type'])

                original_ttl = get_dns_ttl(dns_project_id,
                                           dns_zone_name,
                                           record_name,
                                           record['type'])
                if original_record:
                    remove_record(dns_project_id,
                                  dns_zone_name,
                                  record['type'],
                                  record_name,
                                  original_ttl,
                                  original_record)
                    original_records[record_name] = original_record
                    original_ttls[record_name] = original_ttl

                create_record(dns_project_id,
                              dns_zone_name,
                              record['type'],
                              record_name,
                              record['ttl'],
                              record['value'])
        yield
    finally:
        with dns_transaction(dns_project_id, dns_zone_name):
            for record_name, record in records.items():
                remove_record(dns_project_id,
                              dns_zone_name,
                              record['type'],
                              record_name,
                              record['ttl'],
                              record['value'])
                if original_records and original_records[record_name]:
                    create_record(dns_project_id,
                                  dns_zone_name,
                                  record['type'],
                                  record_name,
                                  original_ttls[record_name],
                                  original_records[record_name])

def has_access_to_dns_zone(dns_project_id, dns_zone):
    result = run_command([
        'gcloud', 'dns', 'managed-zones', 'list',
        ("--filter='name:{}'").format(dns_zone),
        '--format', 'value(name)',
        '--project', dns_project_id])

    if helpers.DRY_RUN:
        return dns_zone
    else:
        if result:
            return result.decode("utf-8").strip()
        return None


def create_dns_zone(custom_domain, dns_zone, dns_project_id):
    LOGGER.info("Creating DNS Zone %s, on domain %s project %s",
                dns_zone, custom_domain, dns_project_id)

    run_command([
        "gcloud", "dns", "managed-zones", "create",
        '--dns-name="{}."'.format(custom_domain),
        '--description="{} A zone" "{}"'.format(custom_domain, dns_zone),
        "--project", dns_project_id
    ])


def retrieve_servers_names(dns_zone, dns_project_id):
    LOGGER.info("Retrieving names servers in %s, project %s",
                dns_zone, dns_project_id)
    returned_servers = run_command_readonly([
        'gcloud', 'dns', 'managed-zones', 'describe',
        dns_zone,
        '--project', dns_project_id
    ])

    servers = returned_servers.decode("utf-8")

    LOGGER.warning("Keep these names servers for the next step\n")
    LOGGER.warning(servers)


def validate_project_access(project_id, exit_code):
    if not has_access_to_project(project_id):
        print(('Project {} not found.'
               'Please check if project id is correct '
               'or if you have been granted access to it.'
               .format(project_id)))
        sys.exit(exit_code)


def get_servers_names(dns_zone, dns_project_id):
    LOGGER.info("Retrieving names servers in %s, project %s",
                dns_zone, dns_project_id)
    returned_servers = run_command_readonly([
        'gcloud', 'dns', 'managed-zones', 'describe',
        dns_zone,
        '--project', dns_project_id,
        "--format='value(nameServers)'"
    ])

    servers = returned_servers.decode("utf-8")\
                .replace("\r", "").replace("\n", "").split(";")

    return servers


def get_dns_ttl(dns_project_id, dns_zone, record_name, record_type):
    ttl = run_command_readonly([
        'gcloud', 'dns', 'record-sets', 'list',
        '--name', record_name,
        '-z', dns_zone,
        '--type', record_type,
        '--format', 'value(ttl)',
        '--project', dns_project_id
    ])
    if ttl:
        return ttl.decode("utf-8").strip()
    return None


def start_transaction(dns_project_id, dns_zone_name):
    LOGGER.info("Starting transaction to %s %s", dns_project_id, dns_zone_name)
    run_command([
        'gcloud', 'dns', 'record-sets',
        'transaction', 'start',
        '-z', dns_zone_name,
        '--project', dns_project_id
    ])

def create_record(dns_project_id, dns_zone_name, record_type,
                  record_name, ttl, records):
    LOGGER.info("Adding %s records on transaction", record_type)

    command = [
        'gcloud', 'dns', 'record-sets', 'transaction', 'add ',
        '-z', dns_zone_name,
        '--name', record_name,
        '--type', record_type,
        '--ttl', ttl
    ]
    if isinstance(records, str):
        command.append("'" + records + "'")
    else:
        for record in records:
            command.append("'" + record + "'")
    command.append('--project')
    command.append(dns_project_id)

    run_command(command)


def remove_record(dns_project_id, dns_zone_name, record_type,
                  record_name, ttl, record_value):
    run_command([
        'gcloud', 'dns', 'record-sets',
        'transaction', 'remove',
        record_value,
        '-z', dns_zone_name,
        '--name', record_name,
        '--type', record_type,
        '--ttl', ttl,
        '--project', dns_project_id
    ])

def execute_transaction(dns_project_id, dns_zone_name):
    run_command([
        'gcloud', 'dns', 'record-sets', 'transaction', 'execute',
        '-z', dns_zone_name,
        '--project', dns_project_id
    ])


def abort_transaction(dns_project_id, dns_zone_name):
    run_command([
        'gcloud', 'dns', 'record-sets', 'transaction', 'abort',
        '-z', dns_zone_name,
        '--project', dns_project_id
    ])


def update_a_record(dns_project_id, dns_zone, record_name, new_ip):
    old_ip = get_dns_record(dns_project_id, dns_zone, record_name, "A")
    with dns_transaction(dns_project_id, dns_zone):
        if old_ip:
            old_ttl = get_dns_ttl(dns_project_id, dns_zone, record_name, "A")
            remove_record(dns_project_id,
                          dns_zone,
                          "A",
                          record_name,
                          old_ttl,
                          old_ip)
        if new_ip:
            create_record(dns_project_id,
                          dns_zone,
                          "A",
                          record_name,
                          "90",
                          new_ip)


def get_dns_record(dns_project_id, dns_zone, record_name, record_type):
    dns_ip = run_command_readonly([
        'gcloud', 'dns', 'record-sets', 'list',
        '--name', record_name,
        '-z', dns_zone,
        '--type', record_type,
        '--format', 'value(DATA)',
        '--project', dns_project_id
    ])
    if dns_ip:
        return dns_ip.decode("utf-8").strip()
    return None


def create_new_dns_record(dns_project_id, dns_zone_name, record_type,
                          record_name, ttl, record_value):
    with dns_transaction(dns_project_id, dns_zone_name):
        create_record(dns_project_id, dns_zone_name, record_type,
                      record_name, ttl, record_value)


def delegate_zone(root_dns_project_id, root_dns_zone_name,
                  delegate_dns_project_id, delegate_dns_zone, custom_domain):
    LOGGER.info("Delegating zone to %s/%s for domain %s",
                root_dns_project_id, root_dns_zone_name, custom_domain)
    records = get_servers_names(delegate_dns_zone, delegate_dns_project_id)
    ttl = get_dns_ttl(delegate_dns_project_id, delegate_dns_zone,
                      custom_domain, "NS")
    create_new_dns_record(root_dns_project_id, root_dns_zone_name,
                          "NS", custom_domain, ttl, records)
