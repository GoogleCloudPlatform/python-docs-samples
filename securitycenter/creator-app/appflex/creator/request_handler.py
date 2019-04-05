from creator.gcp.db_services import get_running_mode, set_running_mode
from creator.query.query_executor import process_saved_queries


def handle_pubsub_request():
    process_saved_queries()


def handle_cron_request():
    mode = get_running_mode()
    print('{} mode'.format(mode))
    if mode == 'PRODUCTION':
        process_saved_queries()
    else:
        print(no_action_mode_message(mode))


def no_action_mode_message(mode):
    if mode == 'DEMO':
        return 'Skipping query execution.'
    return 'No valid mode was found'


def handle_status_config(payload):
    set_running_mode(payload)
