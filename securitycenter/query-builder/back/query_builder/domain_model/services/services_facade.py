from .query_service import (
    run_query_by_uuid as scc_run_by_uuid,
    run_query as scc_run_query,
    save_query as qs_save_query,
    get_query as qs_get_query,
    delete_query as qs_delete_query,
    update_query as qs_update_query,
    list_queries as qs_list_queries,
    update_query_notify as qs_update_query_notify,
    run_scheduled_queries as qs_run_scheduled_queries,
    clean_up_marks as qs_clean_up_marks
)


def save_query(_query):
    if qs_get_query(_query.uuid):
        saved_query = qs_update_query(_query)
    else:
        saved_query = qs_save_query(_query)
        qs_clean_up_marks(_query.uuid)
    return saved_query


def clean_up_marks(uuid):
    qs_clean_up_marks(uuid)


def get_query(uuid):
    return qs_get_query(uuid)


def delete_query(uuid):
    qs_delete_query(uuid)


def list_queries(page=None, page_size=None, text=''):
    return qs_list_queries(page=page, page_size=page_size, text=text)


def run_query(query, mode):
    return scc_run_query(query, mode)


def run_query_by_uuid(uuid):
    return scc_run_by_uuid(uuid)


def run_scheduled_queries():
    return qs_run_scheduled_queries()


def update_query_notify(uuid, flag):
    qs_update_query_notify(uuid, flag)
