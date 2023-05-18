// Copyright 2023 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// This code is internal to the demo.
// It fetches responses from the demo endpoints.
function fetchServerResponse({ body, url }) {
  const serializedBody = JSON.stringify({
    ...body,
  });
  return fetch(url, {
    body: serializedBody,
    headers: new Headers({ "content-type": "application/json" }),
    method: "POST",
  })
    .then((response) => {
      const { ok, body: { data = {} } = {} } = response;
      if (ok) {
        return response.json();
      }
      throw new Error("Response was successful, but status was not 'ok'");
    })
    .then((data) => {
      return data;
    })
    .catch((error) => {
      throw new Error(error);
    });
}

// This code is internal to the demo.
// It passes the score to the demo to display it.
function useAssessmentInClient(score) {
  if (score?.data?.score && score?.data?.label) {
    const demoElement = document.querySelector("recaptcha-demo");
    demoElement.setAttribute("score", score?.data?.score);
    demoElement.setAttribute("label", score?.data?.label);
    demoElement.setAttribute("reason", score?.data?.reason);
  }
}
