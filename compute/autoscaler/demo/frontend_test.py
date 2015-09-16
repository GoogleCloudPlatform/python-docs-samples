# Copyright 2015, Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import unittest

from . import frontend


class FakeTime(object):
    """Fake implementations of GetUserCpuTime, GetUserCpuTime and BusyWait.
    Each call to BusyWait advances both the cpu and the wall clocks by fixed
    intervals (cpu_time_step and wall_time_step, respectively). This can be
    used to simulate arbitrary fraction of CPU time available to the process.
    """
    def __init__(self, cpu_time_step=1.0, wall_time_step=1.0):
        self.cpu_time = 0.0
        self.wall_time = 0.0
        self.cpu_time_step = cpu_time_step
        self.wall_time_step = wall_time_step

    def get_walltime(self):
        return self.wall_time

    def get_user_cputime(self):
        return self.cpu_time

    def busy_wait(self):
        self.wall_time += self.wall_time_step
        self.cpu_time += self.cpu_time_step


class TestHandlers(unittest.TestCase):
    def setUp(self):
        self.fake_time = FakeTime()
        self.cpu_burner = frontend.CpuBurner()
        self.cpu_burner.get_user_cputime = self.fake_time.get_user_cputime
        self.cpu_burner.get_walltime = self.fake_time.get_walltime
        self.cpu_burner.busy_wait = self.fake_time.busy_wait

    # In this test scenario CPU time advances at 25% of the wall time speed.
    # Given the request requires 1 CPU core second, we expect it to finish
    # within the timeout (5 seconds) and return success.
    def test_ok_response(self):
        self.fake_time.cpu_time_step = 0.25
        (code, _) = self.cpu_burner.handle_http_request()
        self.assertEqual(200, code)

    # In this test scenario CPU time advances at 15% of the wall time speed.
    # Given the request requires 1 CPU core second, we expect it to timeout
    # after 5 simulated wall time seconds and return error 500.
    def test_timeout(self):
        self.fake_time.cpu_time_step = 0.15
        (code, _) = self.cpu_burner.handle_http_request()
        self.assertEqual(500, code)


if __name__ == '__main__':
    unittest.main()
