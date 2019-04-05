#!/usr/bin/env python3
"""
Script that creates a sample file
to be used as input on run_setup of query_builder
"""
import json

import click
import colorama
from jsonschema import ValidationError

import helpers
from addresses import get_external_ip
from click_script_commons import (
    configure_helpers,
    instruction_separator,
    parse_args
)
from cluster_handler import create_cluster
from commands import (
    create_file_from_template,
    get_project_number
)
from dns import update_a_record
from kubernetes_handler import (
    apply_kubernetes,
    create_cleanup_configmap,
    create_cloud_sql_credentials_secret,
    create_cloud_sql_instance_secret,
    create_general_configmap,
    create_notification_configmap,
    create_iap_audience_configmap,
    create_scc_account_secret,
    create_scheduler_configmap,
    create_scheduler_credentials_secret,
    create_ssl_secret,
    create_scc_developer_key_secret,
    get_cluster_credentials
)
from network_handler import create_network_infra
from pubsub_handler import (
    create_and_subscribe,
    list_subscriptions
)
from region_validations import get_region_by_zone
from simulation_mode import simulation_wall
from sql_handler import (
    execute_dm_sql_structure,
    execute_storage_flow,
    get_connection_name,
    get_instance_service_account,
    cloud_sql_instance_exists,
    cloud_sql_instance_running,
    start_cloud_sql_instance
)
from validations import json_validation
from validator_handler import (
    validate_project,
    validate_zone,
    validate_in_scope_service_account,
    validate_file_exists,
    validate_dns_zone,
    validate_out_of_scope_service_account,
    validate_cloud_sql)

SUBSCRIPTIONS_PLACEHOLDER = "projects/{}/subscriptions/{}"
TOPICS_PLACEHOLDER = "projects/{}/topics/{}"


colorama.init()


@click.command()
@click.option('--input-file',
              help='Input file', required=True)
@click.option('--source-project',
              help='ProjectId where Query Builder images are available.')
@click.option('--simulation/--no-simulation',
              default=True,
              help='Simulate the execution. Do not execute any command.')
def run_query_builder_setup(simulation, input_file, source_project):
    """ run query builder setup """
    with simulation_wall(simulation):
        try:
            validate_input(input_file)
            click.echo("Input file read from [{}]".format(input_file))
        except ValidationError as json_exception:
            click.echo("Error validating file [{}].".format(input_file))
            click.echo(json_exception)
            return
        except FileNotFoundError as not_found:
            click.echo("File [{0}] not found.".format(not_found.filename))
            return
        except json.decoder.JSONDecodeError as err:
            click.echo("Error parsing file [{0}].\n{1}"
                       .format(input_file, err))
            return

        configure_helpers(simulation)
        query_builder_input = parse_args(input_file)

        validate_arguments(query_builder_input)
        zone = query_builder_input.query_builder.compute_zone
        region = get_region_by_zone(zone)

        static_ip_created = setup_network(
            query_builder_input.query_builder.project_id,
            region,
            query_builder_input.network,
            query_builder_input.use_dm)
        if static_ip_created:
            qb_ip = get_external_ip(
                query_builder_input.query_builder.project_id,
                query_builder_input.network.static_ip
            )
            update_a_record(
                query_builder_input.query_builder.project_id,
                query_builder_input.dns.zone_name,
                query_builder_input.query_builder.custom_domain,
                qb_ip
            )
        setup_sql(query_builder_input.query_builder.project_id,
                  region,
                  query_builder_input.cloud_sql,
                  query_builder_input.use_dm)

        setup_cluster(query_builder_input.query_builder.project_id,
                      query_builder_input.query_builder.compute_zone,
                      query_builder_input.cluster,
                      query_builder_input.network,
                      query_builder_input.use_dm)

        scheduler_topic_name = "scheduler"
        scheduler_topic_path = TOPICS_PLACEHOLDER.format(
            query_builder_input.query_builder.project_id,
            scheduler_topic_name
        )
        scheduler_subscriptions_name = "scheduler-subscription"
        scheduler_subscriptions_path = SUBSCRIPTIONS_PLACEHOLDER.format(
            query_builder_input.query_builder.project_id,
            scheduler_subscriptions_name
        )
        cleanup_topic_name = "cleanup"
        cleanup_topic_path = TOPICS_PLACEHOLDER.format(
            query_builder_input.query_builder.project_id,
            cleanup_topic_name
        )
        cleanup_subscriptions_name = "cleanup-subscription"
        cleanup_subscriptions_path = SUBSCRIPTIONS_PLACEHOLDER.format(
            query_builder_input.query_builder.project_id,
            cleanup_subscriptions_name
        )
        notification_topic_name = "notification"
        notification_topic_path = TOPICS_PLACEHOLDER.format(
            query_builder_input.query_builder.project_id,
            notification_topic_name
        )
        notification_subscriptions_name = "notification-subscription"

        with instruction_separator("Pubsub Infra"):
            setup_pubsub(query_builder_input.query_builder.project_id,
                         notification_topic_name,
                         notification_subscriptions_name,
                         query_builder_input.use_dm)
            setup_pubsub(query_builder_input.query_builder.project_id,
                         scheduler_topic_name,
                         scheduler_subscriptions_name,
                         query_builder_input.use_dm)
            setup_pubsub(query_builder_input.query_builder.project_id,
                         cleanup_topic_name,
                         cleanup_subscriptions_name,
                         query_builder_input.use_dm)

        if source_project:
            query_builder_image_project  = source_project
        else:
            query_builder_image_project = "prod-qb-clsecteam"
        kubernetes_file = "app.yaml"

        generate_kubernetes_file(
            query_builder_input.query_builder.custom_domain,
            query_builder_input.query_builder.version,
            query_builder_image_project,
            get_connection_name(
                query_builder_input.query_builder.project_id,
                query_builder_input.cloud_sql.instance_name),
            kubernetes_file
        )

        with instruction_separator("Cluster Credentials"):
            get_cluster_credentials(
                query_builder_input.query_builder.project_id,
                query_builder_input.cluster.cluster_name,
                query_builder_input.query_builder.compute_zone
            )

        with instruction_separator("Cluster Configurations"):

            create_cluster_configurations(query_builder_input,
                                          scheduler_topic_path,
                                          scheduler_subscriptions_path,
                                          cleanup_topic_path,
                                          cleanup_subscriptions_path,
                                          notification_topic_path)

        with instruction_separator("Kubernetes", "Apply"):
            apply_kubernetes(kubernetes_file)


def validate_input(input_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        json_input = json.loads(infile.read())
        json_validation.validate(json_input)


def validate_arguments(cli_input):
    """Validate all needed properties for the given input"""
    check_zones(cli_input)
    check_projects(cli_input)
    check_service_accounts(cli_input)
    check_ssl_files(cli_input)
    check_dns_zones(cli_input)
    check_cloud_sql(cli_input)


def check_cloud_sql(cli_input):
    """Check if Cloud SQL arguments are valid"""
    if hasattr(cli_input, 'cloud_sql'):
        element_message = 'cloud sql properties'
        validate_cloud_sql(cli_input.cloud_sql, element_message)


def check_dns_zones(cli_input):
    """Check if the given zone belongs to the dns project"""
    if hasattr(cli_input, 'dns'):
        managed_zone = cli_input.dns.zone_name
        dns_project = cli_input.query_builder.project_id
        element_message = 'managed zone: ' + managed_zone
        validate_dns_zone(dns_project, managed_zone, element_message)


def check_ssl_files(cli_input):
    """Check if the given path to SSL files exists"""
    validate_file_exists(cli_input.ssl_certificates.cert_key, 'cert file path')
    validate_file_exists(cli_input.ssl_certificates.private_key,
                         'key file path')


def check_service_accounts(cli_input):
    """Validate all service accounts for the given input, doing a separation of
    in_scope service accounts (the ones that belong to the project under deploy
    and are under control) and out_scope service accounts, which are the ones
    that may have no control under, so a not detailed validation is done
    """
    project = cli_input.query_builder.project_id
    in_scope_service_accounts = [
        cli_input.cloud_sql.service_account,
        cli_input.scheduler.service_account,
        cli_input.notification.service_account
    ]
    in_scope_service_accounts = set(in_scope_service_accounts)
    for service_account in in_scope_service_accounts:
        element_message = 'service account: ' + service_account
        validate_in_scope_service_account(project, service_account,
                                          element_message)
    out_of_scope_service_accounts = [
        cli_input.scc.service_account
    ]
    out_of_scope_service_accounts = set(out_of_scope_service_accounts)
    for service_account in out_of_scope_service_accounts:
        element_message = 'service account: ' + service_account
        validate_out_of_scope_service_account(service_account,
                                              element_message)


def check_zones(cli_input):
    """Validate all zones for the given input"""
    project_id = cli_input.query_builder.project_id
    zones = [
        cli_input.query_builder.compute_zone,
    ]
    zones = set(zones)
    for zone in zones:
        element_message = 'zone: ' + zone
        validate_zone(zone, element_message, project_id)


def check_projects(cli_input):
    """Validate all project ids for the given input"""
    projects = [
        cli_input.query_builder.project_id
    ]
    projects = set(projects)
    for project_id in projects:
        element_message = 'project id: ' + project_id
        validate_project(project_id, element_message)


def setup_pubsub(project, topic_name, subscription_name, use_dm):
    """Execute all needed steps create and subscribe a topic"""
    click.echo('Create topic and subscriptions...')
    create_and_subscribe(project, topic_name, subscription_name, use_dm)
    click.echo('Pubsub configured successfully, check subscription list:')
    click.echo(list_subscriptions())


def setup_sql(project, region, sql_input, use_dm):
    """Execute the steps to enable sql database"""
    step = "Database SQL"
    with instruction_separator(step):
        if cloud_sql_instance_exists(sql_input.instance_name, project):
            if not cloud_sql_instance_running(sql_input.instance_name, project):
                start_cloud_sql_instance(sql_input.instance_name, project)
                connection_name = get_connection_name(project,
                                                      sql_input.instance_name)
                click.echo('Started SQL connection: {}'.format(connection_name))
        else:
            execute_dm_sql_structure(project, sql_input, region, use_dm)
            sql_instance_service_account = get_instance_service_account(
                project,
                sql_input.instance_name)
            execute_storage_flow(project, sql_input, region,
                                 sql_instance_service_account,
                                 helpers.BASE_DIR,
                                 use_dm)
            connection_name = get_connection_name(project,
                                                  sql_input.instance_name)
            click.echo('SQL connection name: {}'.format(connection_name))


def setup_network(project_id, region, network_input, use_dm):
    """Execute the steps to create a network"""
    step = "Network"
    with instruction_separator(step):
        static_ip_created = create_network_infra(project_id, region, network_input, use_dm)
    return static_ip_created


def setup_cluster(project_id, zone, cluster_input, network_input, use_dm):
    """Execute the steps to setup a Cluster"""
    step = "Cluster"
    with instruction_separator(step):
        create_cluster(project_id, zone, cluster_input, network_input, use_dm)


def generate_kubernetes_file(domain, version, image_url, sql_connection_name, output_file_name):
    """ Generate kubernetes file with uer variables """
    template_file_name = "templates/app_yaml.jinja"
    with instruction_separator("Kubernetes File"):
        context = {
            "QB_USER_URL": domain,
            "QB_TAG_VERSION": version,
            "GCR_HOST_PROJECT": image_url,
            "SQL_CONNECTION_NAME": sql_connection_name
        }

        create_file_from_template(template_file_name,
                                  context,
                                  output_file_name)


def create_cluster_configurations(query_builder_input,
                                  scheduler_topic_path,
                                  scheduler_subscriptions_path,
                                  cleanup_topic_path,
                                  cleanup_subscriptions_path,
                                  notification_topic_path):
    """ Create secrets and config maps on cluster """
    create_ssl_secret("querybuilder-ssl-secret",
                      query_builder_input.ssl_certificates.private_key,
                      query_builder_input.ssl_certificates.cert_key)

    create_cloud_sql_instance_secret(
        "cloudsql-instance-credentials",
        query_builder_input.cloud_sql.service_account
    )

    create_cloud_sql_credentials_secret(
        "cloudsql-db-credentials",
        query_builder_input.cloud_sql.user_name,
        query_builder_input.cloud_sql.user_password
    )

    create_scheduler_credentials_secret(
        "scc-scheduler",
        query_builder_input.scheduler.service_account
    )

    create_scheduler_credentials_secret(
        "notification",
        query_builder_input.notification.service_account
    )

    create_scc_developer_key_secret(
        "scc-client-developer-key",
        query_builder_input.scc.developer_key)

    create_scc_account_secret("scc-account",
                              query_builder_input.scc.service_account)

    create_general_configmap("general-config",
                             query_builder_input.organization_id,
                             query_builder_input.organization_display_name,
                             query_builder_input.query_builder.project_id)

    create_notification_configmap("notification-config",
                                  query_builder_input.organization_id,
                                  notification_topic_path)

    create_scheduler_configmap("scheduler-config",
                               scheduler_topic_path,
                               scheduler_subscriptions_path)

    create_cleanup_configmap("cleanup-config",
                             cleanup_topic_path,
                             cleanup_subscriptions_path)
    project_number = get_project_number(
        query_builder_input.query_builder.project_id
    )

    create_iap_audience_configmap(
        "iap-config",
        project_number,
        "backend-service-id"
    )


if __name__ == '__main__':
    run_query_builder_setup()  # pylint: disable=no-value-for-parameter
