"""Creates the backend Environment."""


def GenerateConfig(context):
    """Creates backend properties to configure environment."""
    project = context.properties['project-name']
    endpoint_url = context.properties['endpoint-url']
    status_endpoint_url = context.properties['status_endpoint_url']
    resources = [
        {
            'name': 'publish_processing',
            'type': 'pubsub_topic.py'
        },
        {
            'name': 'demomode',
            'type': 'pubsub_demo.py',
            'properties': {
                'project-name': project,
                'endpoint-url': endpoint_url
            }
        },
        {
            'name': 'publish_status',
            'type': 'pubsub_status.py',
            'properties': {
                'project-name': project,
                'endpoint-url': status_endpoint_url
            }
        }
    ]
    return {'resources': resources}
