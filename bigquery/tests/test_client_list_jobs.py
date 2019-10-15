# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from .. import client_list_jobs
from .. import create_job


def test_client_list_jobs(capsys, client):

    job = create_job.create_job(client)
    client.cancel_job(job.job_id)
    job.cancel()
    client_list_jobs.client_list_jobs(client)
    out, err = capsys.readouterr()
    assert "Started job: {}".format(job.job_id) in out
    assert "Last 10 jobs:" in out
    assert "Jobs from the last ten minutes:" in out
    assert "Last 10 jobs run by all users:" in out
    assert "Last 10 jobs done:" in out
