import argparse

from google.cloud import pubsub


def publish_messages_with_custom_attributes(args):
    """Publishes multiple messages with custom attributes
    to a Pub/Sub topic."""
    publisher = pubsub.PublisherClient()
    topic_path = publisher.topic_path(args.project, args.topic_name)

    with open(args.message_file, 'r') as myfile:
        data = myfile.read().replace('\n', ' ')

    attributes = [line.strip() for line in open(args.attributes_file, 'r')]
    attributes_dict = {k: v for k, v in (x.split('=') for x in attributes)}

    data = data.encode('utf-8')
    publisher.publish(topic_path, data, **attributes_dict)
    print('Published messages with custom attributes.')


def load_arguments():
    _parser = argparse.ArgumentParser(
        description='Publishes to a Pub/Sub topic.')

    _parser.add_argument('-p', '--project',
                         dest='project',
                         help='project where the message will be published',
                         required=True)

    _parser.add_argument('-t', '--topic',
                         dest='topic_name',
                         help='topic where the message will be published',
                         required=True)

    _parser.add_argument('-m', '--message-file',
                         dest='message_file',
                         help='path to the file with message to be published',
                         required=True)

    _parser.add_argument('-a', '--attributes-file',
                         dest='attributes_file',
                         help='path to file with message attributes, in the format key1=value1,key2=value2',
                         required=True)

    return _parser


if __name__ == '__main__':
    print('running publish message')

    parser = load_arguments()
    args = parser.parse_args()
    publish_messages_with_custom_attributes(args)
