import argparse

from google.cloud import pubsub


def list_topics(project):
    """Lists all Pub/Sub topics in the given project."""
    publisher = pubsub.PublisherClient()
    project_path = publisher.project_path(project)

    for topic in publisher.list_topics(project_path):
        print(topic)


def load_arguments():
    _parser = argparse.ArgumentParser(
        description='Lists all topics in the given project')

    _parser.add_argument('-p', '--project',
                         dest='project',
                         help='project where the topic will be created',
                         required=True)

    return _parser


if __name__ == '__main__':
    print('running list topics')

    parser = load_arguments()
    args = parser.parse_args()
    list_topics(args.project)
