# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from datetime import datetime
import random
import string
import time

from google.api_core.exceptions import Aborted
from google.api_core.exceptions import DeadlineExceeded
from google.api_core.exceptions import NotFound
from google.api_core.exceptions import ServiceUnavailable
from google.cloud import monitoring_v3
import pytest
from retrying import retry

import snippets


# We assume we have access to good randomness source.
random.seed()


def random_name(length):
    return "".join([random.choice(string.ascii_lowercase) for i in range(length)])


def retry_on_exceptions(exception):
    return isinstance(exception, (Aborted, ServiceUnavailable, DeadlineExceeded))


def delay_on_aborted(err, *args):
    if retry_on_exceptions(err[1]):
        # add randomness for avoiding continuous conflict
        time.sleep(5 + (random.randint(0, 9) * 0.1))
        return True
    return False


class PochanFixture:
    """A test fixture that creates an alert POlicy and a notification CHANnel,
    hence the name, pochan.
    """

    def __init__(self):
        self.project_id = snippets.project_id()
        self.project_name = snippets.project_name()
        self.alert_policy_client = monitoring_v3.AlertPolicyServiceClient()
        self.notification_channel_client = (
            monitoring_v3.NotificationChannelServiceClient()
        )

        # delete all existing policies older than 1 hour prior to testing
        for policy in self.alert_policy_client.list_alert_policies(name=self.project_name):
            seconds_since_creation = datetime.timestamp(datetime.utcnow())-datetime.timestamp(policy.creation_record.mutate_time)
            if seconds_since_creation > 3600:
                try:
                    self.alert_policy_client.delete_alert_policy(
                        name=policy.name
                    )
                except NotFound:
                    print("Ignored NotFound when deleting a policy.")

    def __enter__(self):
        @retry(
            wait_exponential_multiplier=1000,
            wait_exponential_max=10000,
            stop_max_attempt_number=10,
            retry_on_exception=retry_on_exceptions,
        )
        def setup():
            # Create a policy.
            json = open("test_alert_policy.json").read()
            policy = monitoring_v3.AlertPolicy.from_json(json)
            policy.display_name = "snippets-test-" + random_name(10)
            self.alert_policy = self.alert_policy_client.create_alert_policy(
                name=self.project_name, alert_policy=policy
            )
            # Create a notification channel.
            json = open("test_notification_channel.json").read()
            notification_channel = monitoring_v3.NotificationChannel.from_json(json)
            notification_channel.display_name = "snippets-test-" + random_name(10)
            self.notification_channel = (
                self.notification_channel_client.create_notification_channel(
                    name=self.project_name, notification_channel=notification_channel
                )
            )

        setup()
        return self

    def __exit__(self, type, value, traceback):
        # Delete the policy and channel we created.
        @retry(
            wait_exponential_multiplier=1000,
            wait_exponential_max=10000,
            stop_max_attempt_number=10,
            retry_on_exception=retry_on_exceptions,
        )
        def teardown():
            try:
                self.alert_policy_client.delete_alert_policy(
                    name=self.alert_policy.name
                )
            except NotFound:
                print("Ignored NotFound when deleting a policy.")
            try:
                if self.notification_channel.name:
                    self.notification_channel_client.delete_notification_channel(
                        self.notification_channel.name
                    )
            except NotFound:
                print("Ignored NotFound when deleting a channel.")

        teardown()


@pytest.fixture(scope="session")
def pochan():
    with PochanFixture() as pochan:
        yield pochan


def test_list_alert_policies(capsys, pochan):
    # Query snippets.list_alert_policies() for up to 50 seconds
    # to allow the newly created policy to appear in the list.
    retry = 5
    while retry:
        snippets.list_alert_policies(pochan.project_name)
        out, _ = capsys.readouterr()
        if pochan.alert_policy.display_name in out:
            break
        retry = retry - 1
        time.sleep(10)

    assert retry > 0


@pytest.mark.flaky(rerun_filter=delay_on_aborted, max_runs=5)
def test_enable_alert_policies(capsys, pochan):
    # These sleep calls are for mitigating the following error:
    # "409 Too many concurrent edits to the project configuration.
    # Please try again."
    # Having multiple projects will void these `sleep()` calls.
    # See also #3310
    time.sleep(2)
    snippets.enable_alert_policies(pochan.project_name, True, f"name='{pochan.alert_policy.name}'")
    out, _ = capsys.readouterr()
    assert (
        f"Enabled {pochan.project_name}" in out
        or f"{pochan.alert_policy.name} is already enabled" in out
    )

    time.sleep(2)
    snippets.enable_alert_policies(pochan.project_name, False, f"name='{pochan.alert_policy.name}'")
    out, _ = capsys.readouterr()
    assert (
        f"Disabled {pochan.project_name}" in out
        or f"{pochan.alert_policy.name} is already disabled" in out
    )


@pytest.mark.flaky(rerun_filter=delay_on_aborted, max_runs=5)
def test_replace_channels(capsys, pochan):
    alert_policy_id = pochan.alert_policy.name.split("/")[-1]
    notification_channel_id = pochan.notification_channel.name.split("/")[-1]

    # This sleep call is for mitigating the following error:
    # "409 Too many concurrent edits to the project configuration.
    # Please try again."
    # Having multiple projects will void this `sleep()` call.
    # See also #3310
    time.sleep(2)
    snippets.replace_notification_channels(
        pochan.project_name, alert_policy_id, [notification_channel_id]
    )
    out, _ = capsys.readouterr()
    assert f"Updated {pochan.alert_policy.name}" in out


@pytest.mark.flaky(rerun_filter=delay_on_aborted, max_runs=5)
@pytest.mark.skip(reason="Needs fixing by CODEOWNER - issue #8975")
def test_backup_and_restore(capsys, pochan):
    # These sleep calls are for mitigating the following error:
    # "409 Too many concurrent edits to the project configuration.
    # Please try again."
    # Having multiple projects will void this `sleep()` call.
    # See also #3310
    time.sleep(2)
    snippets.backup(pochan.project_name, "backup.json")
    out, _ = capsys.readouterr()

    time.sleep(2)
    snippets.restore(pochan.project_name, "backup.json")
    out, _ = capsys.readouterr()
    assert f"Updated {pochan.alert_policy.name}" in out
    assert (
        f"Updating channel {pochan.notification_channel.display_name}" in out
    )


@pytest.mark.flaky(rerun_filter=delay_on_aborted, max_runs=5)
def test_delete_channels(capsys, pochan):
    notification_channel_id = pochan.notification_channel.name.split("/")[-1]

    # This sleep call is for mitigating the following error:
    # "409 Too many concurrent edits to the project configuration.
    # Please try again."
    # Having multiple projects will void these `sleep()` calls.
    # See also #3310
    time.sleep(2)
    snippets.delete_notification_channels(
        pochan.project_name, [notification_channel_id], force=True
    )
    out, _ = capsys.readouterr()
    assert f"{notification_channel_id} deleted" in out
    pochan.notification_channel.name = ""  # So teardown is not tried
