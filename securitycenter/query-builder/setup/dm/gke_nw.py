"""Manages the network creation"""


def GenerateConfig(context):
    """Creates and configures network properties"""
    region = context.properties['region']
    network_name = context.properties['network']
    subnet_name = context.properties['subnetwork']
    subnet_range_1 = context.properties['subnet_range_1']
    subnet_range_pods = context.properties['subnet_range_pods']
    subnet_range_services = context.properties['subnet_range_services']

    resources = [
        {
            'name': network_name,
            'type': 'network_template.py'
        },
        {
            'name': subnet_name,
            'type': 'subnetwork_template.py',
            'properties': {
                'network': network_name,
                'region': region,
                'ipRange': subnet_range_1,
                'secondaryIpRanges': [
                    {
                        'rangeName': subnet_name + '-pods',
                        'ipCidrRange': subnet_range_pods,
                    }, {
                        'rangeName': subnet_name + '-services',
                        'ipCidrRange': subnet_range_services,
                    }
                ]
            }
        }
    ]
    return {'resources': resources}
