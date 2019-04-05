import argparse

from google.cloud import pubsub


def list_subscriptions_in_topic(project, topic_name):
    """Lists all subscriptions for a given topic."""
    subscriber = pubsub.PublisherClient()
    topic_path = subscriber.topic_path(project, topic_name)

    for subscription in subscriber.list_topic_subscriptions(topic_path):
        print(subscription)


def list_subscriptions_in_project(project):
    """Lists all subscriptions in the current project."""
    subscriber = pubsub.SubscriberClient()
    project_path = subscriber.project_path(project)

    for subscription in subscriber.list_subscriptions(project_path):
        print(subscription.name)


def load_arguments():
    _parser = argparse.ArgumentParser(description='Lists subscriptions')

    _parser.add_argument('-p', '--project',
                         dest='project',
                         help='project where the subscritpions will be searched',
                         required=True)

    _parser.add_argument('-t', '--topic',
                         dest='topic_name',
                         help='topic where the subscritpions will be searched')

    return _parser


if __name__ == '__main__':
    print('running list subscriptions')

    parser = load_arguments()
    args = parser.parse_args()
    if args.topic_name:
        list_subscriptions_in_topic(args.project, args.topic_name)
    else:
        list_subscriptions_in_project(args.project)
