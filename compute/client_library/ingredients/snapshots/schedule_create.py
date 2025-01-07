#  Copyright 2024 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# This is an ingredient file. It is not meant to be run directly. Check the samples/snippets
# folder for complete code samples that are ready to be used.
# Disabling flake8 for the ingredients file, as it would fail F821 - undefined name check.
# flake8: noqa

from google.cloud import compute_v1


# <INGREDIENT create_schedule_snapshots>
def snapshot_schedule_create(
    project_id: str,
    region: str,
    schedule_name: str,
    schedule_description: str,
    labels: dict,
) -> compute_v1.ResourcePolicy:
    """
    Creates a snapshot schedule for disks for a specified project and region.
    Args:
        project_id (str): The ID of the Google Cloud project.
        region (str): The region where the snapshot schedule will be created.
        schedule_name (str): The name of the snapshot schedule group.
        schedule_description (str): The description of the snapshot schedule group.
        labels (dict): The labels to apply to the snapshots. Example: {"env": "dev", "media": "images"}
    Returns:
        compute_v1.ResourcePolicy: The created resource policy.
    """

    # # Every hour, starts at 12:00 AM
    # hourly_schedule = compute_v1.ResourcePolicyHourlyCycle(
    #     hours_in_cycle=1, start_time="00:00"
    # )
    #
    # # Every Monday, starts between 12:00 AM and 1:00 AM
    # day = compute_v1.ResourcePolicyWeeklyCycleDayOfWeek(
    #     day="MONDAY", start_time="00:00"
    # )
    # weekly_schedule = compute_v1.ResourcePolicyWeeklyCycle(day_of_weeks=[day])

    # In this example we use daily_schedule - every day, starts between 12:00 AM and 1:00 AM
    daily_schedule = compute_v1.ResourcePolicyDailyCycle(
        days_in_cycle=1, start_time="00:00"
    )

    schedule = compute_v1.ResourcePolicySnapshotSchedulePolicySchedule()
    # You can change the schedule type to daily_schedule, weekly_schedule, or hourly_schedule
    schedule.daily_schedule = daily_schedule

    # Autodelete snapshots after 5 days
    retention_policy = compute_v1.ResourcePolicySnapshotSchedulePolicyRetentionPolicy(
        max_retention_days=5
    )
    snapshot_properties = (
        compute_v1.ResourcePolicySnapshotSchedulePolicySnapshotProperties(
            guest_flush=False, labels=labels
        )
    )

    snapshot_policy = compute_v1.ResourcePolicySnapshotSchedulePolicy()
    snapshot_policy.schedule = schedule
    snapshot_policy.retention_policy = retention_policy
    snapshot_policy.snapshot_properties = snapshot_properties

    resource_policy_resource = compute_v1.ResourcePolicy(
        name=schedule_name,
        description=schedule_description,
        snapshot_schedule_policy=snapshot_policy,
    )

    client = compute_v1.ResourcePoliciesClient()
    operation = client.insert(
        project=project_id,
        region=region,
        resource_policy_resource=resource_policy_resource,
    )
    wait_for_extended_operation(operation, "Resource Policy creation")

    return client.get(project=project_id, region=region, resource_policy=schedule_name)


# </INGREDIENT>
