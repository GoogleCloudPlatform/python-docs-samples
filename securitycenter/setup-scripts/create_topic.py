import argparse

from google.cloud import pubsub


def create_topic(project, topic_name):
    """Create a new Pub/Sub topic."""
    publisher = pubsub.PublisherClient()
    topic_path = publisher.topic_path(project, topic_name)
    topic = publisher.create_topic(topic_path)
    print('Topic created: {}'.format(topic))


def load_arguments():
    _parser = argparse.ArgumentParser(description='Create a pub/sub topic')

    _parser.add_argument('-p', '--project',
                         dest='project',
                         help='project where the topic will be created',
                         required=True)

    _parser.add_argument('-t', '--topic',
                         dest='topic_name',
                         help='the name of the topic',
                         required=True)
    return _parser


if __name__ == '__main__':
    print('running create topic')

    parser = load_arguments()
    args = parser.parse_args()
    create_topic(args.project, args.topic_name)
