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

const SUBMIT_URLS = {
  comment: "on_comment_submit",
  home: "on_homepage_load",
  login: "on_login",
  signup: "on_signup",
  store: "on_store_checkout",
  game: undefined,
};

async function homepage({token}) {
  const json_body = JSON.stringify({
    recaptcha_cred: {
      token: token,
    },
  });
  // Fetch the demo assessment from backend.
  const score = await fetchDemoAssessment({
    url: SUBMIT_URLS.home,
    json_body: json_body,
  });
  useAssessment(score);
}

async function signup({token}) {
  // Do not pass plain text credentials. Always encrypt and follow security standards.
  // Obtain the values from your form data.
  const json_body = JSON.stringify({
    recaptcha_cred: {
      token: token,
      username: "",
      password: "",
    },
  });
  // Fetch the demo assessment from backend.
  const score = await fetchDemoAssessment({
    url: SUBMIT_URLS.signup,
    json_body: json_body,
  });
  useAssessment(score);
}

async function login({token}) {
  // Do not pass plain text credentials. Always encrypt and follow security standards.
  // Obtain the values from your form data.
  const json_body = JSON.stringify({
    recaptcha_cred: {
      token: token,
      username: "",
      password: "",
    },
  });
  // Fetch the demo assessment from backend.
  const score = await fetchDemoAssessment({
    url: SUBMIT_URLS.login,
    json_body: json_body,
  });
  useAssessment(score);
}

async function store({token}) {
  // Do not pass plain text credentials. Always encrypt and follow security standards.
  // Obtain the values from your form data.
  const json_body = JSON.stringify({
    recaptcha_cred: {
      token: token,
      items: {}.toString(),
    },
  });
  // Fetch the demo assessment from backend.
  const score = await fetchDemoAssessment({
    url: SUBMIT_URLS.store,
    json_body: json_body,
  });
  useAssessment(score);
}

async function comment({token}) {
  // Do not pass plain text credentials. Always encrypt and follow security standards.
  // Obtain the values from your form data.
  const json_body = JSON.stringify({
    recaptcha_cred: {
      token: token,
      comment: "",
    },
  });
  // Fetch the demo assessment from backend.
  const score = await fetchDemoAssessment({
    url: SUBMIT_URLS.comment,
    json_body: json_body,
  });
  useAssessment(score);
}

function fetchDemoAssessment({ url, json_body}) {
  // Code for fetching the assessment from backend goes here.
  // Refer to demo app backend code for more information.
  // See if using a library or framework, can use event handlers its usual way.
  // See: https://cloud.google.com/recaptcha-enterprise/docs/create-assessment
  return fetch(`/${url}`, {
    body: json_body,
    method: "POST",
    headers: new Headers({'content-type': 'application/json'}),
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

function useAssessment(score) {
  // Code for handling the assessment goes here.
  showAssessmentInDemo(score);
}

function showAssessmentInDemo(score) {
  if (score?.data?.score && score?.data?.verdict) {
    const demoElement = document.querySelector("recaptcha-demo");
    demoElement.setAttribute("score", score?.data?.score);
    demoElement.setAttribute("verdict", score?.data?.verdict);
  }
}