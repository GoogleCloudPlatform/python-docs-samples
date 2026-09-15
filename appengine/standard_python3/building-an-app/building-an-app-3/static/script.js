/**
 * Copyright 2018, Google LLC
 * Licensed under the Apache License, Version 2.0 (the `License`);
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an `AS IS` BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
'use strict';

// [START gae_python38_auth_javascript]
// [START gae_python3_auth_javascript]
window.addEventListener('load', function () {
  document.getElementById('sign-out').onclick = function () {
    firebase.auth().signOut();
  };

  // Initialize the FirebaseUI Widget outside of onAuthStateChanged
  // to avoid multiple instantiation errors when logging out and back in.
  var ui = firebaseui.auth.AuthUI.getInstance() || new firebaseui.auth.AuthUI(firebase.auth());

  // FirebaseUI config.
  var uiConfig = {
    signInSuccessUrl: '/',
    signInOptions: [
      // Comment out any lines corresponding to providers you did not check in
      // the Firebase console.
      firebase.auth.GoogleAuthProvider.PROVIDER_ID,
      firebase.auth.EmailAuthProvider.PROVIDER_ID,
      //firebase.auth.FacebookAuthProvider.PROVIDER_ID,
      //firebase.auth.TwitterAuthProvider.PROVIDER_ID,
      //firebase.auth.GithubAuthProvider.PROVIDER_ID,
      //firebase.auth.PhoneAuthProvider.PROVIDER_ID
    ],
    // Terms of service url.
    tosUrl: '<your-tos-url>',
    // Add callbacks to handle successful sign in before redirecting
    callbacks: {
      signInSuccessWithAuthResult: function (authResult, redirectUrl) {
        // Wait for the token to be fetched before redirecting to ensure the backend gets it.
        authResult.user.getIdToken().then(function (token) {
          // Set the cookie with a path so it applies globally
          document.cookie = "token=" + token + ";path=/";
          window.location.assign(redirectUrl || '/');
        });
        // Return false to prevent Firebase UI from redirecting automatically
        return false; 
      }
    }
  };

  firebase.auth().onAuthStateChanged(function (user) {
    if (user) {
      // User is signed in, so display the "sign out" button and login info.
      document.getElementById('sign-out').hidden = false;
      document.getElementById('login-info').hidden = false;
      console.log(`Signed in as ${user.displayName} (${user.email})`);
      user.getIdToken().then(function (token) {
        // Add the token to the browser's cookies. The server will then be
        // able to verify the token against the API.
        // SECURITY NOTE: As cookies can easily be modified, only put the
        // token (which is verified server-side) in a cookie; do not add other
        // user information.
        document.cookie = "token=" + token + ";path=/";
      });
    } else {
      // User is signed out.
      // Show the Firebase login button.
      ui.start('#firebaseui-auth-container', uiConfig);
      // Update the login state indicators.
      document.getElementById('sign-out').hidden = true;
      document.getElementById('login-info').hidden = true;
      // Clear the token cookie safely.
      document.cookie = "token=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;SameSite=Lax";
    }
  }, function (error) {
    console.log(error);
    alert('Unable to log in: ' + error)
  });
});
// [END gae_python3_auth_javascript]
// [END gae_python38_auth_javascript]
