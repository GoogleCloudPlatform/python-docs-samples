def GenerateConfig(context):

    resources = [{
        'name': 'cron-custom-role',
        'type': 'gcp-types/iam-v1:organizations.roles',
        'properties': {
            'parent': 'organizations/' + context.properties['organizationId'],
            'roleId': 'custom.cron.appCreator',
            'role': {
                'title': 'CR - Google Cron Application Creator',
                'description': 'Custom cron app to Create Google App Engine Applications.',
                'stage': 'BETA',
                'includedPermissions': [
                    'appengine.applications.list',
                    'appengine.memcache.addKey',
                    'appengine.memcache.flush',
                    'appengine.memcache.get',
                    'appengine.memcache.getKey',
                    'appengine.memcache.list',
                    'appengine.memcache.update',
                ]
            }
        }
    }]

    return {
        'resources': resources
    }
