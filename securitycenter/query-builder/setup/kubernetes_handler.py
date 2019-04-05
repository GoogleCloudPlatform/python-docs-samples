import helpers
from base import (run_command)


def get_cluster_credentials(project_id, cluster_name, zone_name):
    """
    Gets cluster crendentials on  project.
        :param project_id: string project_id
        :param cluster_name: string cluster_name
    """
    cmd = [
        "gcloud", "container", "clusters",
        "get-credentials", cluster_name,
        "--zone", zone_name,
        "--project", project_id
    ]
    run_command(cmd)


def create_ssl_secret(secret_name, ssl_key, ssl_cert):
    """
    Creates SSL secret on cluster
        :param secret_name: string: name of secret
        :param ssl_key: path to SSL key file
        :param ssl_cert: path to SSL cert file
    """
    cmd = [
        "kubectl", "create", "secret", "tls", secret_name,
        "--key", ssl_key,
        "--cert", ssl_cert
    ]
    run_command(cmd)


def create_scc_account_secret(secret_name, scc_credentials):
    """
    Creates SCC credentials secret on cluster
        :param secret_name: string: name of secret
        :param scc_credentials: path to SCC credentials file
    """
    cmd = [
        "kubectl", "create", "secret", "generic", secret_name,
        "--from-file=scc-credentials={}".format(scc_credentials)
    ]
    run_command(cmd)


def create_cloud_sql_instance_secret(secret_name, cloud_sql_instance_credentials):
    """
    Creates Cloud SQL Instance credential's secret on cluster
        :param secret_name: string: name of secret
        :param cloud_sql_instance_credentials: path to Cloud SQL Instance credentials file
    """
    cmd = [
        "kubectl", "create", "secret", "generic", secret_name,
        "--from-file=credentials.json={}".format(cloud_sql_instance_credentials)
    ]
    run_command(cmd)


def create_cloud_sql_credentials_secret(secret_name, username, password):
    """
    Creates Cloud SQL Database Credentials secret on cluster
        :param secret_name: string: name of secret
        :param username: string database username
        :param password: string database password
    """
    cmd = [
        "kubectl", "create", "secret", "generic", secret_name,
        "--from-literal=username={}".format(username),
        "--from-literal=password={}".format(password)
    ]
    run_command(cmd)


def create_scc_developer_key_secret(secret_name, developer_key):
    """
    Creates Cloud SQL Database Credentials secret on cluster
        :param secret_name: string: name of secret
        :param developer_key: developer key to access SCC
    """
    cmd = [
        "kubectl", "create", "secret", "generic", secret_name,
        "--from-literal=developer-key={}".format(developer_key),
    ]
    run_command(cmd)


def create_scheduler_credentials_secret(secret_name, pubsub_credentials):
    """
    Creates Scheduler credentials secret on cluster
        :param secret_name: string: name of secret
        :param pubsub_credentials: path to pubsub credentials file
    """
    cmd = [
        "kubectl", "create", "secret", "generic", secret_name,
        "--from-file=pubsub.credentials={}".format(pubsub_credentials),
        "--from-file=notifier.credentials={}".format(pubsub_credentials)
    ]
    run_command(cmd)


def create_general_configmap(configmap_name, organization_id,
                             organization_display_name, project_id):
    """
    Creates general configmap on cluster
        :param configmap_name: string: name of configmap
        :param organization_id: string organization id
        :param organization_display_name: string organization display name
        :param project_id: string query builder project id
    """
    cmd = [
        "kubectl", "create", "configmap", configmap_name,
        "--from-literal=organization_id={}".format(organization_id),
        "--from-literal=organization_display_name={}".format(organization_display_name),
        "--from-literal=project_id={}".format(project_id)
    ]
    run_command(cmd)


def create_notification_configmap(configmap_name, organization_id, notification_topic):
    """
    Create config map to notification app
        :param configmap_name: string: name of config map
        :param organization_id: string: organization id
        :param notification_topic: string: notification topic
    """
    cmd = [
        "kubectl", "create", "configmap", configmap_name,
        "--from-literal=organization_id={}".format(organization_id),
        "--from-literal=notification_topic={}".format(notification_topic)
    ]
    run_command(cmd)


def create_scheduler_configmap(configmap_name, scheduler_topic_path, scheduler_subscriptions_path):
    """
    Creates schedulers configmap
        :param configmap_name: string: name of config map
        :param scheduler_topic_path: string: path of scheduler's topic
        :param scheduler_subscriptions_name: path of subscription
    """
    cmd = [
        "kubectl", "create", "configmap", configmap_name,
        "--from-literal=topic.name={}".format(scheduler_topic_path),
        "--from-literal=subscriptions.name={}".format(scheduler_subscriptions_path)
    ]
    run_command(cmd)


def create_cleanup_configmap(configmap_name, cleanup_topic_path, cleanup_subscriptions_path):
    """
    Creates Cleanup configmap
        :param configmap_name: string: name of config map
        :param cleanup_topic_path: string: path of cleanup's topic
        :param cleanup_subscriptions_path: path of subscription
    """
    cmd = [
        "kubectl", "create", "configmap", configmap_name,
        "--from-literal=topic.name={}".format(cleanup_topic_path),
        "--from-literal=subscriptions.name={}".format(cleanup_subscriptions_path)
    ]
    run_command(cmd)


def create_iap_audience_configmap(configmap_name, project_number, backend_service):
    """
    Creates IAP Audience configmap
        :param configmap_name:  string: name of config map
        :param project_number: string: project number of Load Balancer
        :param backend_service: string: name of backend service of Load Balancer
    """
    cmd = [
        "kubectl", "create", "configmap", configmap_name,
        "--from-literal=iap.audience=/projects/{}/global/backendServices/{}"\
        .format(project_number, backend_service)
    ]
    run_command(cmd)

def apply_kubernetes(file_path):
    """
    Apply one or more kubernetes file, it can be a file path or a directory path
        :param file_path: string: file path or a directory path
    """
    cmd = [
        "kubectl", "apply", "-f",
        file_path
    ]
    run_command(cmd)


def delete_configmap(configmap_name):
    """
    Delete a configmap on cluster
        :param configmap_name: string: name of configmap
    """
    cmd = [
        "kubectl", "delete", "configmap", configmap_name
    ]
    run_command(cmd)


def delete_secret(secret_name):
    """
    Delete a configmap on cluster
        :param secret_name: string: name of secret
    """
    cmd = [
        "kubectl", "delete", "secret", secret_name
    ]
    run_command(cmd)


def patch_deployment(deployment_name, value):
    """
    Patchs a deployment using merge stratagy
    """
    run_command([
        "kubectl", "patch", "deployment",
        deployment_name, "-p", value
    ])
