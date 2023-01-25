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

function createAssessment({ action, sitekey, token }) {
    const body = JSON.stringify({
      recaptcha_cred: {
        action,
        sitekey,
        token,
      },
    });
    console.log({ body });
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
        console.log(data);
        return data;
      })
      .catch((error) => {
        console.error(error);
        throw new Error(error);
      });
  }
  
  // TODO: possible global getToken with ready/execute
  
  function useAssessment(score) {
    console.log("useAssessment", score);
    document
      .querySelector("recaptcha-demo")
      .setAttribute("score", score.data.score);
    document
      .querySelector("recaptcha-demo")
      .setAttribute("verdict", score.data.verdict);
  }
  