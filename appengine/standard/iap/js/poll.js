// Copyright 2017 Google LLC
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

"use strict";

function getStatus() {
  var statusElm = document.getElementById('status');
  statusElm.innerHTML = 'Polling';
  fetch('/status').then(function(response) {
    if (response.ok) {
      return response.text();
    }
    // [START gae_handle_error]
    if (response.status === 401) {
      statusElm.innerHTML = 'Login stale. <input type="button" value="Refresh" onclick="sessionRefreshClicked();"/>';
    }
    // [END gae_handle_error]
    else {
      statusElm.innerHTML = response.statusText;
    }
    throw new Error (response.statusText);
  })
  .then(function(text) {
    statusElm.innerHTML = text;
  })
  .catch(function(statusText) {
  });
}

getStatus();
setInterval(getStatus, 10000); // 10 seconds

// [START gae_refresh_session]
var iapSessionRefreshWindow = null;

function sessionRefreshClicked() {
  if (iapSessionRefreshWindow == null) {
    iapSessionRefreshWindow = window.open("/?gcp-iap-mode=DO_SESSION_REFRESH");
    window.setTimeout(checkSessionRefresh, 500);
  }
  return false;
}

function checkSessionRefresh() {
  if (iapSessionRefreshWindow != null && !iapSessionRefreshWindow.closed) {
    // Attempting to start a new session.
    // XMLHttpRequests is used by the server to identify AJAX requests
    fetch('/favicon.ico', {
          method: "GET",
          credentials: 'include',
          headers: {
              'X-Requested-With': 'XMLHttpRequest'
          }
    .then((response) => {
      // Checking if browser has a session for the requested app
      if (response.status === 401) {
        // No new session detected. Try to get a session again
        window.setTimeout(checkSessionRefresh, 500);
      } else {
        // Session retrieved.
        iapSessionRefreshWindow.close();
        iapSessionRefreshWindow = null;
      }
    })
    });
  } else {
    iapSessionRefreshWindow = null;
  }
}
// [END gae_refresh_session]
