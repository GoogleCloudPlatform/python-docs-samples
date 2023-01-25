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
  