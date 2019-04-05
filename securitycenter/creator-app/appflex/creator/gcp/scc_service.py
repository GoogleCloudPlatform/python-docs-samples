import client.scc_client_beta as beta_api
from creator.config_service import get_current_organization


def get_scc_client(organization_id):
    return beta_api.Client(organization_id)


def execute_cscc_search(kind, query_args):
    client = get_scc_client(get_current_organization())
    if kind == 'ASSET':
        return client.list_assets(filter_expression=query_args.get('query'),
                                  read_time=query_args.get('reference_time'),
                                  compare_duration=query_args.get('compare_duration'))
    if kind == 'FINDING':
        return client.list_findings(source='-',
                                    filter_expression=query_args.get('query'),
                                    read_time=query_args.get('reference_time'))
