import json
import helpers
from base import run_command_readonly, run_command
from commands import get_command_result


def get_backend_service(project_id, _filter, value='name'):
    result_ = run_command_readonly([
        'gcloud', 'compute', 'backend-services', 'list',
        '--project', project_id,
        "--format",
        "value({})".format(value),
        "--filter='{}'".format(_filter)
    ])
    return result_.decode("utf-8").strip()


def get_backend_service_id(project_id, service_name):
    return get_backend_service(project_id, service_name, value='id')


def network_exists(network_name, project):
    command_ = [
        'gcloud', 'compute', 'networks', 'list',
        '--filter ', 'name=' + network_name,
        '--project', project,
        '--format', 'json'
    ]
    return get_command_result(command_)


def default_network_has_no_instances(project):
    result_ = run_command_readonly([
        'gcloud', 'compute', 'instances', 'list',
        '--filter', '"networkInterfaces[].network:default"',
        '--format', 'json',
        '--project', project,
    ])
    return result_.decode("utf-8").strip() == '[]'


def sub_network_exists(sub_network_name, project):
    command_ = [
        'gcloud', 'compute', 'networks', 'subnets', 'list',
        '--filter', 'name=' + sub_network_name,
        '--project', project,
        '--format', 'json'
    ]
    return get_command_result(command_)


def static_ip_exists(static_ip, project):
    command_ = [
        'gcloud', 'compute', 'addresses', 'list',
        '--filter', 'NAME=' + static_ip,
        '--project', project,
        '--format', 'json'
    ]
    return get_command_result(command_)


def delete_backend_service(project_id, backend_service_name):
    run_command([
        'gcloud', 'compute', 'backend-services', 'delete',
        backend_service_name,
        '--project', project_id
    ])


def list_backend_services(project_id):
    result_ = run_command_readonly([
        'gcloud', 'compute', 'backend-services', 'list',
        '--project', project_id,
        "--format='json(name)'"
    ])
    return json.loads(result_.decode("utf-8").strip())


def list_target_proxies(project_id, protocol):
    result_ = run_command_readonly([
        'gcloud', 'compute', "target-{}-proxies".format(protocol), 'list',
        '--project', project_id,
        "--format='json(name)'"
    ])
    return json.loads(result_.decode("utf-8").strip())


def delete_target_proxy(project_id, protocol, target_proxie_name):
    run_command([
        'gcloud', 'compute', "target-{}-proxies".format(protocol), 'delete',
        target_proxie_name,
        '--project', project_id
    ])


def list_forwarding_rules(project_id):
    result_ = run_command_readonly([
        'gcloud', 'compute', "forwarding-rules", 'list',
        '--project', project_id,
        "--format='json(name)'"
    ])
    return json.loads(result_.decode("utf-8").strip())


def delete_forwarding_rules(project_id, rule_name):
    run_command([
        'gcloud', 'compute', "forwarding-rules", 'delete', rule_name,
        '--project', project_id
    ])


def list_health_checks(project_id):
    result_ = run_command_readonly([
        'gcloud', 'compute', "health-checks", 'list',
        '--project', project_id,
        "--format='json(name)'"
    ])
    return json.loads(result_.decode("utf-8").strip())


def delete_health_check(project_id, health_checks_name):
    run_command([
        'gcloud', 'compute', "health-checks", 'delete',
        health_checks_name,
        '--project', project_id
    ])


def list_url_maps(project_id):
    result_ = run_command_readonly([
        'gcloud', 'compute', "url-maps", 'list',
        '--project', project_id,
        "--format='json(name)'"
    ])
    return json.loads(result_.decode("utf-8").strip())


def delete_url_maps(project_id, url_maps_name):
    run_command([
        'gcloud', 'compute', "url-maps", 'delete', url_maps_name,
        '--project', project_id
    ])