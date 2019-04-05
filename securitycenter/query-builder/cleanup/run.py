import os
import json
from pytz import utc

from google.cloud import pubsub
from google.oauth2 import service_account as sa

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from settings import configure_logger
from cleanup_service import (
    pull_messages,
    clean_temp_marks,
    clean_marks_by_uuid
)

MISSING_ENV_VAR_ERROR_MESSAGE = "Application not running: missing required env vars."

LOGGER = configure_logger('cleanup')
CLEAN_ALL_CRON_EXPRESSION = os.getenv('CLEAN_ALL_CRON_EXPRESSION', '*/15 * * * *')
CLEAN_UUID_CRON_EXPRESSION = os.getenv('CLEAN_ALL_CRON_EXPRESSION', '* * * * *')
SUBSCRIPTION_NAME = os.getenv('SUBSCRIPTION_NAME')
CREDENTIALS = os.getenv('PUBSUB_CREDENTIALS')


def __start_task():
    credentials = __get_credentials()
    subscriber = pubsub.SubscriberClient(credentials=credentials)
    future = subscriber.subscribe(SUBSCRIPTION_NAME,
                                  pull_messages)
    scheduler = BlockingScheduler(timezone=utc)
    scheduler.add_job(clean_temp_marks,
                      CronTrigger.from_crontab(CLEAN_ALL_CRON_EXPRESSION))
    scheduler.add_job(clean_marks_by_uuid,
                      CronTrigger.from_crontab(CLEAN_UUID_CRON_EXPRESSION))
    LOGGER.info('clean up started')
    try:
        scheduler.start()
        future.result()
    except Exception as ex:
        LOGGER.error(ex)
        raise
    except (KeyboardInterrupt, SystemExit):
        future.cancel()
        LOGGER.info('exiting application')


def __get_credentials():
    credential_json = json.loads(CREDENTIALS)
    return sa.Credentials.from_service_account_info(credential_json)


if __name__ == '__main__':
    if SUBSCRIPTION_NAME:
        __start_task()
    else:
        LOGGER.error(MISSING_ENV_VAR_ERROR_MESSAGE)
        raise ValueError(MISSING_ENV_VAR_ERROR_MESSAGE)
