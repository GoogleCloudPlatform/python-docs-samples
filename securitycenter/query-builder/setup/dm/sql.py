"""Creates the sql instance database and set user."""


def GenerateConfig(context):
    """Creates sql properties to configure database environment."""
    instance_name = context.properties['instance_name']
    region = context.properties['region']
    tier = context.properties['tier']

    database_name = context.properties['database_name']
    charset = context.properties['charset']
    database_dependency = [instance_name]

    user_name = context.properties['user_name']
    user_password = context.properties['user_password']
    user_resource_name = context.properties['user_resource_name']
    user_dependency = [database_name]

    resources = [
        {
            'name': 'db-qb-instance',
            'type': 'sql_instance.py',
            'properties': {
                'name': instance_name,
                'region': region,
                'tier': tier
            }
        },
        {
            'name': 'qb-database',
            'type': 'sql_database.py',
            'properties': {
                'name': database_name,
                'instance': instance_name,
                'charset': charset,
                'depends': database_dependency
            }
        },
        {
            'name': 'qb-proxyuser',
            'type': 'sql_user.py',
            'properties': {
                'resource_name': user_resource_name,
                'user_name': user_name,
                'user_password': user_password,
                'instance': instance_name,
                'depends': user_dependency
            }
        }
    ]
    return {'resources': resources}
