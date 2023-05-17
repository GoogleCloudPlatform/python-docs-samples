import list_logs
import os

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]


def test_list_logs(capsys):
    logs = list_logs.list_logs(PROJECT)
    assert "logs" in str(logs)
