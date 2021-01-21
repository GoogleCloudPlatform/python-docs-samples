import os

import googleapiclient.discovery

import check_latest_transfer_operation


def test_latest_transfer_operation(capsys):
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]

    transfer_job = {
        "description": "Sample job",
        "status": "ENABLED",
        "projectId": project_id,
        "schedule": {
            "scheduleStartDate": {"day": "01", "month": "01", "year": "2000"},
            "startTimeOfDay": {"hours": "00", "minutes": "00", "seconds": "00"},
        },
        "transferSpec": {
            "gcsDataSource": {"bucketName": project_id + "-storagetransfer-source"},
            "gcsDataSink": {"bucketName": project_id + "-storagetransfer-sink"},
            "objectConditions": {
                "minTimeElapsedSinceLastModification": "2592000s"  # 30 days
            },
            "transferOptions": {"deleteObjectsFromSourceAfterTransfer": "true"},
        },
    }
    storagetransfer = googleapiclient.discovery.build("storagetransfer", "v1")
    result = storagetransfer.transferJobs().create(body=transfer_job).execute()

    job_name = result.get("name")
    check_latest_transfer_operation.check_latest_transfer_operation(
        project_id, job_name
    )
    out, _ = capsys.readouterr()

    assert job_name in out
