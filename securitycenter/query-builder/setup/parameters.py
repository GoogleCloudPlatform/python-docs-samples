"""
Parameters passed to Query Builder Input
"""
QUERY_BUILDER_INPUT = {
    "organization_id": "your-organization-id",
    "organization_display_name": "your-organization-display-name",
    "use_dm": False,

    "query_builder": {
        "compute_zone": "us-central1-a",
        "project_id": "query_builder_project_id",
        "custom_domain": "custom_domain",
        "version": "v3.3.0"
    },

    "oauth": {
        "client_id": "client_id",
        "client_secret": "client_secret",
    },

    "dns": {  # this can be optional
        "zone_name": "dns_zone_name"
    },

    "scc": {
        "service_account": "file_path.json",
        "developer_key": "developer_key"
    },

    "scheduler": {
        "service_account": "file_path.json"
    },

    "notification": {
        "service_account": "file_path.json"
    },

    "cloud_sql": {
        "instance_name": "db-qb-instance",
        "tier": "db-n1-standard-2",
        "database_name": "query_builder",
        "charset": "utf8",
        "user_name": "user_name",
        "user_password": "user_password",
        "user_resource_name": "db-qb-proxyuser",
        "service_account": "file_path.json"
    },

    "network": {
        "network_name": "scc-tools-nw",
        "sub_network_name": "scc-tools-subnet",
        "static_ip": "querybuilder-web-static-ip",
        "subnet_range_1": "10.1.0.0/19",
        "subnet_range_pods": "10.2.0.0/19",
        "subnet_range_services": "10.3.0.0/22",
    },

    "ssl_certificates": {
        "cert_key": "cert1.pem",
        "private_key": "privkey1.pem",
    },

    "cluster": {
        "cluster_name": "scc-tools-gke-cluster",
        "node_pool_name": "scc-tools-gke-cluster-pool",
        "cluster_ip": "10.56.0.0/14",
        "machine_type": "n1-highcpu-8",
        "min_nodes": "1",
        "max_nodes": "3",
        "timeout": "3600"
    }
}
