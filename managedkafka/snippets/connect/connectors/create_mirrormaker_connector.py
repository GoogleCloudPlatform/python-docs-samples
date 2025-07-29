def create_mirrormaker_connector(
    project_id: str,
    region: str,
    connect_cluster_id: str,
    connector_id: str,
    topics: str,
    source_cluster_alias: str,
    target_cluster_alias: str,
    source_bootstrap_servers: str,
    target_bootstrap_servers: str,
    offset_syncs_topic_replication_factor: str,
    source_cluster_security_protocol: str,
    source_cluster_sasl_mechanism: str,
    source_cluster_sasl_login_callback_handler_class: str,
    source_cluster_sasl_jaas_config: str,
    target_cluster_security_protocol: str,
    target_cluster_sasl_mechanism: str,
    target_cluster_sasl_login_callback_handler_class: str,
    target_cluster_sasl_jaas_config: str,
) -> None:
    """
    Create a MirrorMaker 2.0 connector with SASL/OAUTHBEARER security.

    Args:
        project_id: Google Cloud project ID.
        region: Cloud region.
        connect_cluster_id: ID of the Kafka Connect cluster.
        connector_name: Name of the connector.
        topics: Topics to mirror.
        source_cluster_alias: Alias for the source cluster.
        target_cluster_alias: Alias for the target cluster.
        source_bootstrap_servers: Source cluster bootstrap servers.
        target_bootstrap_servers: Target cluster bootstrap servers.
        offset_syncs_topic_replication_factor: Replication factor for offset-syncs topic.
        source_cluster_security_protocol: Security protocol for source cluster.
        source_cluster_sasl_mechanism: SASL mechanism for source cluster.
        source_cluster_sasl_login_callback_handler_class: SASL login callback handler class for source cluster.
        source_cluster_sasl_jaas_config: SASL JAAS config for source cluster.
        target_cluster_security_protocol: Security protocol for target cluster.
        target_cluster_sasl_mechanism: SASL mechanism for target cluster.
        target_cluster_sasl_login_callback_handler_class: SASL login callback handler class for target cluster.
        target_cluster_sasl_jaas_config: SASL JAAS config for target cluster.

    Raises:
        This method will raise the GoogleAPICallError exception if the operation errors.
    """
    # TODO(developer): Update with your config values. Here is a sample configuration:
    # project_id = "my-project-id"
    # region = "us-central1"
    # connect_cluster_id = "my-connect-cluster"
    # connector_id = "MM2_CONNECTOR_ID"
    # topics = "GMK_TOPIC_NAME"
    # source_cluster_alias = "source"
    # target_cluster_alias = "target"
    # source_bootstrap_servers = "GMK_SOURCE_CLUSTER_DNS"
    # target_bootstrap_servers = "GMK_TARGET_CLUSTER_DNS"
    # offset_syncs_topic_replication_factor = "1"
    # source_cluster_security_protocol = "SASL_SSL"
    # source_cluster_sasl_mechanism = "OAUTHBEARER"
    # source_cluster_sasl_login_callback_handler_class = "com.google.cloud.hosted.kafka.auth.GcpLoginCallbackHandler"
    # source_cluster_sasl_jaas_config = "org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required;"
    # target_cluster_security_protocol = "SASL_SSL"
    # target_cluster_sasl_mechanism = "OAUTHBEARER"
    # target_cluster_sasl_login_callback_handler_class = "com.google.cloud.hosted.kafka.auth.GcpLoginCallbackHandler"
    # target_cluster_sasl_jaas_config = "org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required;"

    # [START managedkafka_create_mirrormaker2_connector]
    from google.api_core.exceptions import GoogleAPICallError
    from google.cloud.managedkafka_v1.services.managed_kafka_connect import (
        ManagedKafkaConnectClient,
    )
    from google.cloud.managedkafka_v1.types import Connector, CreateConnectorRequest

    connect_client = ManagedKafkaConnectClient()
    parent = connect_client.connect_cluster_path(project_id, region, connect_cluster_id)

    configs = {
        "connector.class": "org.apache.kafka.connect.mirror.MirrorSourceConnector",
        "source.cluster.alias": source_cluster_alias,
        "target.cluster.alias": target_cluster_alias,
        "topics": topics,
        "source.cluster.bootstrap.servers": source_bootstrap_servers,
        "target.cluster.bootstrap.servers": target_bootstrap_servers,
        "offset-syncs.topic.replication.factor": offset_syncs_topic_replication_factor,
        "source.cluster.security.protocol": source_cluster_security_protocol,
        "source.cluster.sasl.mechanism": source_cluster_sasl_mechanism,
        "source.cluster.sasl.login.callback.handler.class": source_cluster_sasl_login_callback_handler_class,
        "source.cluster.sasl.jaas.config": source_cluster_sasl_jaas_config,
        "target.cluster.security.protocol": target_cluster_security_protocol,
        "target.cluster.sasl.mechanism": target_cluster_sasl_mechanism,
        "target.cluster.sasl.login.callback.handler.class": target_cluster_sasl_login_callback_handler_class,
        "target.cluster.sasl.jaas.config": target_cluster_sasl_jaas_config,
    }

    connector = Connector()
    connector.name = connector_id
    connector.configs = configs

    request = CreateConnectorRequest(
        parent=parent,
        connector_id=connector_id,
        connector=connector,
    )

    try:
        operation = connect_client.create_connector(request=request)
        print(f"Waiting for operation {operation.operation.name} to complete...")
        response = operation.result()
        print("Created Connector:", response)
    except GoogleAPICallError as e:
        print(f"The operation failed with error: {e}")
    # [END managedkafka_create_mirrormaker2_connector]
