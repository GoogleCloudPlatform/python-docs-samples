"""
For this module to be executed, the following environment variables must be
previously set:

* SUBSCRIPTION_NAME: name of the created subscription, in the format
                     projects/{project_id}/subscriptions/{id}

Also, the following environment variables may be previously set:

* QB_BACK_URL_PROTOCOL: SCC-Query-Builder server protocol
* QB_BACK_URL_HOST: SCC-Query-Builder server host
* QB_BACK_URL_PORT: SCC-Query-Builder server port

"""
import os
import json
from pytz import utc
from google.cloud import pubsub
from google.oauth2 import service_account as sa

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from scheduled_queries_executor import (
    pull_queries,
    execute_run_scheduled_queries,
    trigger_scheduled_queries
)
import default_settings

LOGGER = default_settings.configure_logger('run')

MISSING_ENV_VAR_ERROR_MESSAGE = \
    "Application not running: missing required env vars." \
    " See module docstring for details."

QUERIES_CRON_EXPRESSION = os.getenv('QUERIES_CRON_EXPRESSION', '* * * * *')
SUBSCRIPTION_NAME = os.getenv('SUBSCRIPTION_NAME')
CREDENTIALS = os.getenv('PUBSUB_CREDENTIALS')


def __process_scheduled_queries():
    credentials = __get_credentials()
    subscriber = pubsub.SubscriberClient(credentials=credentials)
    future = subscriber.subscribe(SUBSCRIPTION_NAME,
                                  pull_queries)
    scheduler = BlockingScheduler(timezone=utc)
    scheduler.add_job(trigger_scheduled_queries,
                      trigger=CronTrigger.from_crontab(QUERIES_CRON_EXPRESSION),
                      name='Trigger the scheduled queries to run')
    scheduler.add_job(execute_run_scheduled_queries,
                      trigger=CronTrigger.from_crontab(QUERIES_CRON_EXPRESSION),
                      name='Call the Query builder to run scheduled queries')
    LOGGER.info('Schedule started')
    try:
        scheduler.start()
        future.result()
    except Exception as ex:
        LOGGER.error(ex)
        raise
    except (KeyboardInterrupt, SystemExit):
        future.cancel()
        LOGGER.info('Exiting application')


def __get_credentials():
    credential_json = json.loads(CREDENTIALS)
    return sa.Credentials.from_service_account_info(credential_json)


if __name__ == '__main__':
    if SUBSCRIPTION_NAME:
        __process_scheduled_queries()
    else:
        LOGGER.error(MISSING_ENV_VAR_ERROR_MESSAGE)
        raise ValueError(MISSING_ENV_VAR_ERROR_MESSAGE)
