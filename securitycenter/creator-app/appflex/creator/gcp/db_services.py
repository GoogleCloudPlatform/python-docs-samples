from google.cloud import datastore

from creator.config_service import get_namespace


def create_ds_client():
    return datastore.Client(namespace=get_namespace())


def get_event_queries():
    ds_client = create_ds_client()
    return ds_client.query(
        kind='EventQuery'
    ).fetch()


def get_running_mode():
    ds_client = create_ds_client()
    processing_status = list(ds_client.query(
        kind='ProcessingStatus'
    ).fetch(1))
    return processing_status[0]['status'] if processing_status else 'NOT_FOUND'


def set_running_mode(payload):
    ds_client = create_ds_client()
    key = ds_client.key('ProcessingStatus', 'processing_status_key')
    entity = datastore.Entity(key)
    entity['status'] = payload['status']
    ds_client.put(entity)
    print('Processing status set to: {}'.format(entity['status']))


def get_query_last_execution(query):
    ds_client = create_ds_client()
    key = ds_client.key('EventQueryExecution', query.key.id_or_name)
    query = ds_client.query(kind='EventQueryExecution')
    query.add_filter('__key__', '=', key)
    response = list(query.fetch(1))
    if response:
        return response[0]['lastExecution']
    return None


def set_query_last_execution(query, last_execution):
    ds_client = create_ds_client()
    key = ds_client.key('EventQueryExecution', query.key.id_or_name)
    entity = datastore.Entity(key)
    entity['lastExecution'] = last_execution
    ds_client.put(entity)
