import argparse

import googleapiclient.discovery


def list_clusters_and_nodepools(project_id, zone):
    """Lists all clusters and associated node pools."""
    service = googleapiclient.discovery.build('container', 'v1')
    clusters_resource = service.projects().zones().clusters()

    clusters_response = clusters_resource.list(
        projectId=project_id, zone=zone).execute()

    for cluster in clusters_response.get('clusters', []):
        print('Cluster: {}, Status: {}, Current Master Version: {}'.format(
            cluster['name'], cluster['status'],
            cluster['currentMasterVersion']))

        nodepools_response = clusters_resource.nodePools().list(
            projectId=project_id, zone=zone,
            clusterId=cluster['name']).execute()

        for nodepool in nodepools_response['nodePools']:
            print(
                ' -> Pool: {}, Status: {}, Machine Type: {}, '
                'Autoscaling: {}'.format(
                    nodepool['name'], nodepool['status'],
                    nodepool['config']['machineType'],
                    nodepool.get('autoscaling', {}).get('enabled', False)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')
    list_clusters_and_nodepools_parser = subparsers.add_parser(
        'list_clusters_and_nodepools',
        help=list_clusters_and_nodepools.__doc__)
    list_clusters_and_nodepools_parser.add_argument('project_id')
    list_clusters_and_nodepools_parser.add_argument('zone')

    args = parser.parse_args()

    if args.command == 'list_clusters_and_nodepools':
        list_clusters_and_nodepools(args.project_id, args.zone)
    else:
        parser.print_help()
