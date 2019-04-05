from google.cloud import datastore
import os


def create_ds_client(namespace=None):
    project_id = os.getenv('creator_project_id')
    
    if namespace:
        return datastore.Client(project=project_id, namespace=namespace)
    
    return datastore.Client(project_id)


def list_all_from_kind(namespace='scccreator', kind='EventQuery'):
    ds_client = create_ds_client(namespace)
    task = ds_client.query(kind=kind)
    task_results = list(task.fetch())
    return task_results


def delete_all_from_kind(namespace='scccreator', kind='EventQuery'):
    ds_client = create_ds_client(namespace)
    queries = list_all_from_kind()
    keys = []
    for query in queries:
      keys.append(query.key)
    ds_client.delete_multi(keys)


def delete_record(key, namespace='scccreator', kind='EventQuery'):
    ds_client = create_ds_client(namespace)
    key = ds_client.key(kind, key)
    ds_client.delete(key)


def add_records(items_array, properties_array, namespace='scccreator', kind='EventQuery'):
    ds_client = create_ds_client(namespace)
    key = ds_client.key(kind)
    for item in items_array:
        entity = datastore.Entity(key)
        set_entity_properties(entity, item, properties_array)
        ds_client.put(entity)
        print('{} record added: {}'.format(kind, entity))


def set_entity_properties(entity, base_obj, properties):
    for prop in properties:
        entity[prop] = base_obj[prop]