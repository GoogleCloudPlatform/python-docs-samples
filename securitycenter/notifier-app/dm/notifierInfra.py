"""Creates cloud function, topic and subscription."""


def GenerateConfig(context):
    """Creates cloud function, topic and subscription to deal with notifications."""
    resources = [{
        'name': context.properties['function_name'],
        'type': 'cloud_function.py',
        'properties': {
            'region': context.properties['region'],
            'function_name': context.properties['function_name'],
            'bucket': context.properties['cf_bucket'],
        }
    }]

    if ('True' != context.properties['skip_pubsub']):
        resources.extend([{
            'name': context.properties['topic_name'],
            'type': 'pubsub_topic.py'
        }, {
            'name': context.properties['subscriber_name'],
            'type': 'pubsub_subscriber.py',
            'properties': {
                'topic_name': context.properties['topic_name'],
                'endpoint_url': context.properties['endpoint_url']
            }
        }])

    return {'resources': resources}
