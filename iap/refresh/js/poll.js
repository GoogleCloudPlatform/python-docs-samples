// Copyright Google Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

(function poll() {
  setTimeout(function() {
    var statusText = document.getElementById('status');
    statusText.innerHTML = 'Polling';
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/status');
    xhr.onload = function(){
      if (xhr.status === 200) {
        statusText.innerHTML = xhr.response;
      } else
      // [START handle_error]
      if (xhr.status === 401) {
        statusText.innerHTML = 'Login stale. <input type="button" value="Refresh" onclick="session_refresh_clicked();"/>';
      }
      // [END handle_error]
      else {
        statusText.innerHTML = xhr.statusText;
      }
      poll();
    };
    xhr.send(null);
  }, 10000);
})();

// [START refresh_session]
var iap_session_refresh_window = null;

function session_refresh_clicked() {
  if (iap_session_refresh_window == null) {
    iap_session_refresh_window = window.open("/_gcp_iap/do_session_refresh");
    window.setTimeout(check_session_refresh, 500);
  }
  return false;
}

function check_session_refresh() {
  if (iap_session_refresh_window != null && !iap_session_refresh_window.closed) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/favicon.ico');
    xhr.onload = function(){
      if (xhr.status === 401) {
        // Session is still stale.
        window.setTimeout(check_session_refresh, 500);
      } else {
        iap_session_refresh_window.close();
        iap_session_refresh_window = null;
      }
    };
    xhr.send(null);
  } else {
    iap_session_refresh_window = null;
  }
}
// [END refresh_session]
