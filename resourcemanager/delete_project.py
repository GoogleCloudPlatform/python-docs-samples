from utils import build_client
import argparse


def run(id):
    client = build_client()
    project = client.projects().delete(projectId=id)
    if project['lifecycleState'] == 'DELETE_REQUESTED':
        print("Project {} successfully deleted".format(id))
    else:
        print("""Project {} was not scheduled for deletion:
              either the project is associated with a billing account,
              or is not currently active""".format(id))


parser = argparse.ArgumentParser(description='Delete a Google Cloud Project')
parser.add_argument('--id',
                    type=str,
                    required=True,
                    help='Unique Id of the project to delete')

if __name__ == '__main__':
    args = parser.parse_args()
    run(args.id)
