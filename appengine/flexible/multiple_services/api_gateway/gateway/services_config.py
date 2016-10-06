import os

#to add services insert key value pair of the name of the service and
#the port you want it to run on when running locally
SERVICES = {
    'default': 5000,
    'static': 8001
}

def map_services(environment):
    url_map = {}
    for service, local_port in SERVICES.items():
        if environment == 'production':
            url_map[service] = production_url(service)
        if environment == 'development':
            url_map[service] = local_url(local_port)
    return url_map

def production_url(service_name):
    project_id = os.environ.get('GAE_LONG_APP_ID') or 'flask-algo'
    project_url = project_id + '.appspot.com'
    template = 'https://{}{}'
    if service_name == 'default':
        return template.format('', project_url)
    else:
        return template.format(service_name + '-dot-', project_url)

def local_url(port):
    return 'http://localhost:' + str(port)
