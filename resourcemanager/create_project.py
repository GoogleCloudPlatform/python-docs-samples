from utils import build_client, wait_for_active
from googleapiclient.errors import HttpError
import httplib2
import random
import argparse
import json


def create_project(name, id, **labels):
    return client.projects().create(body={
            'projectId': pid_candidate,
            'name': name
            'labels': labels
            }).execute()


    def run(name, id=None, **labels):
        project = None
    if id is None:
        while project is None:
            id = "{}-{}-{}".format(*rw.random_words(count=2),
                                   random.randint(100, 999))[:30]
            try:
                project = create_project(client, name, id, **labels)
            except HttpError as e:
                code, uri, reason = str(e).parse(
                        '<HttpError %s when requesting %s returned "%s">')
                if not reason == "Requested entity already exists":
                    raise e
    else:
        project = create_project(client, name, id, **labels)

    return wait_for_active(project)


parser = argparse.ArgumentParser(description = 'Create a Google Cloud Project')
parser.add_argument('--name',
                    type=str,
                    help='Human readable name of the project',
                    required=True)
parser.add_argument('--id',
                    type=str,
                    help="""Unique ID of the project. Max 30 Characters.
                    Only hyphens, digits, and lower case letters.
                    Leave blank to use a generated string""")
parser.add_argument('--labels',
                    type=json.loads,
                    help='Json formatted dictionary of labels')

if __name__=='__main__':
    args = parser.parse_args()
   if args.labels:
       run(args.name, id=args.id, **args.labels)
   else:
       run(args.name, id=args.id)
