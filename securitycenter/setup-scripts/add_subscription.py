import argparse

from google.cloud import pubsub
from google.cloud.pubsub_v1.types import PushConfig


def load_arguments():
    _parser = argparse.ArgumentParser(description='Adding topic subscription')
    _parser.add_argument('-t', '--topic_name',
                         dest='topic_name',
                         required=True,
                         help='The topic name in which the subscription will attach to')
    _parser.add_argument('-s', '--subscription_name',
                         dest='subscription_name',
                         required=True,
                         help='The subscription name to be created')
    _parser.add_argument('-tp', '--topic_project',
                         dest='topic_project',
                         required=True,
                         help='The project of the referred topic.')
    _parser.add_argument('-sp', '--subscription_project',
                         dest='subscription_project',
                         required=True,
                         help='The project of the subscription.')
    _parser.add_argument('-e', '--push_endpoint',
                         dest='push_endpoint',
                         help='Endpoint to be connected to the subscription in the Push-style. '
                              'If not informed, will use Pull-style')
    return _parser


def add_subscription(topic_project, topic_name, subscription_project, subscription_name, push_endpoint):
    push_config = None
    if push_endpoint:
        push_config = PushConfig()
        push_config.push_endpoint = push_endpoint
    subscriber = pubsub.SubscriberClient()
    topic = 'projects/{}/topics/{}'.format(topic_project, topic_name)
    subscription = 'projects/{}/subscriptions/{}'.format(subscription_project, subscription_name)
    subscription = subscriber.create_subscription(subscription, topic, push_config)
    print('Subscription created: {}'.format(subscription))


if __name__ == '__main__':
    print('Adding new subscription')
    parser = load_arguments()
    args = parser.parse_args()
    add_subscription(
        args.topic_project,
        args.topic_name,
        args.subscription_project,
        args.subscription_name,
        args.push_endpoint
    )
