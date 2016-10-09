import os
import requests
import services_config

app = services_config.make_app(__name__)

@app.route('/')
def root():
    '''Gets index.html from the static file server'''
    res = requests.get(app.config['SERVICE_MAP']['static'])
    return res.content

@app.route('/hello/<service>')
def say_hello(service):
    '''Recieves requests from buttons on the front end and resopnds
    or sends request to the static file server'''
    #if 'gateway' is specified return immediate
    if service == 'gateway':
        return 'Gateway says hello'
    #otherwise send request to service indicated by URL param
    responses = []
    url = app.config['SERVICE_MAP'][service]
    res = requests.get(url + '/hello')
    responses.append(res.content)
    return '\n'.encode().join(responses)

@app.route('/<path>')
def static_file(path):
    '''Gets static files required by index.html to static file server'''
    url = app.config['SERVICE_MAP']['static']
    res = requests.get(url + '/' + path)
    return res.content, 200, {'Content-Type': res.headers['Content-Type']}

if __name__ == '__main__':
    port = os.environ.get('PORT') or 8000
    app.run(port=port)
