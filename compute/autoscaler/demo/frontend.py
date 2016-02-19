# Copyright 2015, Google, Inc.
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

"""A simple web server which responds to HTTP GET requests by consuming CPU.
This binary runs in a GCE VM. It serves HTTP requests on port 80. Every request
with path '/service' consumes 1 core-second of CPU time, with the timeout of
5 (walltime) seconds. The purpose of this application is to demonstrate how
Google Compute Engine Autoscaler can scale a web frontend server based on CPU
utilization.
The original version of this file is available here:
https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/compute/
    autoscaler/demo/tests/test_frontend.py
"""

try:
    import BaseHTTPServer
    import SocketServer
except:
    import http.server as BaseHTTPServer
    import socketserver as SocketServer

from multiprocessing import Process
import os
import sys
import time

REQUEST_CPUTIME_SEC = 1.0
REQUEST_TIMEOUT_SEC = 5.0


class CpuBurner(object):
    def get_walltime(self):
        return time.time()

    def get_user_cputime(self):
        return os.times()[0]

    def busy_wait(self):
        for _ in range(100000):
            pass

    def burn_cpu(self):
        """Consume REQUEST_CPUTIME_SEC core seconds.
        This method consumes REQUEST_CPUTIME_SEC core seconds. If unable to
        complete within REQUEST_TIMEOUT_SEC walltime seconds, it times out and
        terminates the process.
        """
        start_walltime_sec = self.get_walltime()
        start_cputime_sec = self.get_user_cputime()
        while (self.get_user_cputime() <
               start_cputime_sec + REQUEST_CPUTIME_SEC):
            self.busy_wait()
            if (self.get_walltime() >
                    start_walltime_sec + REQUEST_TIMEOUT_SEC):
                sys.exit(1)

    def handle_http_request(self):
        """Process a request to consume CPU and produce an HTTP response."""
        start_time = self.get_walltime()
        p = Process(target=self.burn_cpu)  # Run in a separate process.
        p.start()
        # Force kill after timeout + 1 sec.
        p.join(timeout=REQUEST_TIMEOUT_SEC + 1)
        if p.is_alive():
            p.terminate()
        if p.exitcode != 0:
            return (500, "Request failed\n")
        else:
            end_time = self.get_walltime()
            response = "Request took %.2f walltime seconds\n" % (
                end_time - start_time)
            return (200, response)


class DemoRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """Request handler for Demo http server."""

    def do_GET(self):
        """Handle an HTTP GET request."""
        mapping = {
            "/": lambda: (200, "OK"),  # Return HTTP 200 response.
            "/service": CpuBurner().handle_http_request,
        }
        if self.path not in mapping:
            self.send_response(404)
            self.end_headers()
            return
        (code, response) = mapping[self.path]()
        self.send_response(code)
        self.end_headers()
        self.wfile.write(response)
        self.wfile.close()


class DemoHttpServer(SocketServer.ThreadingMixIn,
                     BaseHTTPServer.HTTPServer):
    pass


if __name__ == "__main__":
    httpd = DemoHttpServer(("", 80), DemoRequestHandler)
    httpd.serve_forever()
