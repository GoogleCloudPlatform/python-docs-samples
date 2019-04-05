import os
import requests

import default_settings

LOGGER = default_settings.configure_logger('scheduled_queries_executor')

QB_BACK_URL_PROTOCOL = os.getenv('QB_BACK_URL_PROTOCOL', 'http')
QB_BACK_URL_HOST = os.getenv('QB_BACK_URL_HOST', 'localhost')
QB_BACK_URL_PORT = os.getenv('QB_BACK_URL_PORT', '8080')

QUERY_UUID_LIST = []


def __add_to_be_processed(query_uuid):
    if QUERY_UUID_LIST.count(query_uuid) < 1:
        QUERY_UUID_LIST.append(query_uuid)


def pull_queries(message):
    """
    This is a callback function for PubSub
    :param message: message received from PubSub
    """
    query_uuid = message.data.decode('utf-8')
    LOGGER.info("Received query id: %s", query_uuid)
    __add_to_be_processed(query_uuid)
    message.ack()


def execute_run_scheduled_queries():
    """
    Call the query builder backend service endpoint to execute scheduled
    queries.
    It will call the endpoint as long as there's query UUIDs recorded at
    QUERY_UUID_LIST.
    If any error occurs, or it's returned a HTTP status code different from
    200, it will log it.
    """
    LOGGER.info("Execute scheduled queries")
    while QUERY_UUID_LIST:
        query_uuid = QUERY_UUID_LIST.pop()
        try:
            LOGGER.info("Calling /queries/run/%s", query_uuid)
            response = requests.post('{}://{}:{}/queries/run/{}'
                                     .format(QB_BACK_URL_PROTOCOL,
                                             QB_BACK_URL_HOST,
                                             QB_BACK_URL_PORT,
                                             query_uuid),
                                     headers={"x-goog-authenticated-user-email": "scheduler@example.org",
                                              "x-goog-authenticated-user-id": "accounts.google.com",
                                              "x-goog-iap-jwt-assertion": "jwttoken"})
            if response.status_code != 200:
                LOGGER.error("Could not run query: %s due to %s",
                             query_uuid, response)
        except Exception as ex:
            LOGGER.error("Could not run query: %s", query_uuid)
            LOGGER.error(ex)


def trigger_scheduled_queries():
    """
    Call the query builder backend service endpoint to trigger the scheduled
    queries search.
    If any error occurs, or it's returned a HTTP status code different from
    200, it will log it.
    """
    try:
        LOGGER.info("Calling /queries/scheduled/run")
        response = requests.put('{}://{}:{}/queries/scheduled/run'
                                .format(QB_BACK_URL_PROTOCOL,
                                        QB_BACK_URL_HOST,
                                        QB_BACK_URL_PORT),
                                headers={"x-goog-authenticated-user-email": "scheduler@example.org",
                                         "x-goog-authenticated-user-id": "accounts.google.com",
                                         "x-goog-iap-jwt-assertion": "jwttoken"})
        if response.status_code != 200:
            LOGGER.error("Could not run scheduled queries due to %s",
                         response)
    except Exception as ex:
        LOGGER.error(ex)
