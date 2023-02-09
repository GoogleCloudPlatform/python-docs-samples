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

// ATTENTION: reCAPTCHA Example (Part 3) Starts
// SEE: https://cloud.google.com/recaptcha-enterprise/docs/create-assessment
// SEE: If using a library or famework, can use event handlers its usual way

function createAssessment({ action, token }) {
  // SEE: Code for fetching the assessment from backend goes here
  // SEE: Refer to demo app backend code for more information
  // SEE: If using a library or framework, can fetch its usual way
  return fetchDemoAssessment({ action, token });
}

function useAssessment(score) {
  // SEE: Code for handling the assessment goes here
  showAssessmentInDemo(score);
}

// ATTENTION: reCAPTCHA Example (Part 3) Ends

function fetchDemoAssessment({ action, token }) {
  const body = JSON.stringify({
    recaptcha_cred: {
      action,
      token,
    },
  });
  return fetch("/create_assessment", {
    body,
    method: "POST",
  })
    .then((response) => {
      const { ok, body: { data = {} } = {} } = response;
      if (ok) {
        return response.json();
      }
    })
    .then((data) => {
      return data;
    })
    .catch((error) => {
      throw new Error(error);
    });
}

function showAssessmentInDemo(score) {
  if (score?.data?.score && score?.data?.verdict) {
    const demoElement = document.querySelector("recaptcha-demo");
    demoElement.setAttribute("score", score?.data?.score);
    demoElement.setAttribute("verdict", score?.data?.verdict);
  }
}

// TODO: possible global getToken with ready/execute
