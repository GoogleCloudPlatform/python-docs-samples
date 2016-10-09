import os
from flask import Flask

#to add services insert key value pair of the name of the service and
#the port you want it to run on when running locally
SERVICES = {
    'default': 8000,
    'static': 8001
}

def make_app(name):
    app = Flask(name)
    environment = 'production' if os.environ.get('GAE_LONG_APP_ID') else 'development'
    app.config['SERVICE_MAP'] = map_services(environment)
    return app

def map_services(environment):
    '''Generates a map of services to correct urls for running locally
    or when deployed'''
    url_map = {}
    for service, local_port in SERVICES.items():
        if environment == 'production':
            url_map[service] = production_url(service)
        if environment == 'development':
            url_map[service] = local_url(local_port)
    return url_map

def production_url(service_name):
    '''Generates url for a service when deployed to App Engine'''
    project_id = os.environ.get('GAE_LONG_APP_ID')
    project_url = '{}.appspot.com'.format(project_id)
    if service_name == 'default':
        return 'https://{}'.format(project_url)
    else:
        return 'https://{}-dot-{}'.format(service_name, project_url)

def local_url(port):
    '''Generates url for a service when running locally'''
    return 'http://localhost:{}'.format(str(port))
