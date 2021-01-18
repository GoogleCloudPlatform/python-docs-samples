firebase.initializeApp(config);

// Watch for state change from sign in
function initApp() {
  firebase.auth().onAuthStateChanged(user => {
    if (user) {
      // User is signed in.
      document.getElementById('signInButton').innerText = 'Sign Out';
      document.getElementById('form').style.display = '';
    } else {
      // No user is signed in.
      document.getElementById('signInButton').innerText = 'Sign In with Google';
      document.getElementById('form').style.display = 'none';
    }
  });
}
window.onload = function () {
  initApp();
};

// [START cloudrun_end_user_firebase_sign_in]
// [START run_end_user_firebase_sign_in]
function signIn() {
  const provider = new firebase.auth.GoogleAuthProvider();
  provider.addScope('https://www.googleapis.com/auth/userinfo.email');
  firebase
    .auth()
    .signInWithPopup(provider)
    .then(result => {
      // Returns the signed in user along with the provider's credential
      console.log(`${result.user.displayName} logged in.`);
      window.alert(`Welcome ${result.user.displayName}!`);
    })
    .catch(err => {
      console.log(`Error during sign in: ${err.message}`);
      window.alert(`Sign in failed. Retry or check your browser logs.`);
    });
}
// [END run_end_user_firebase_sign_in]
// [END cloudrun_end_user_firebase_sign_in]

function signOut() {
  firebase
    .auth()
    .signOut()
    .then(result => {})
    .catch(err => {
      console.log(`Error during sign out: ${err.message}`);
      window.alert(`Sign out failed. Retry or check your browser logs.`);
    });
}

// Toggle Sign in/out button
function toggle() {
  if (!firebase.auth().currentUser) {
    signIn();
  } else {
    signOut();
  }
}

// [START cloudrun_end_user_token]
// [START run_end_user_token]
async function vote(team) {
  if (firebase.auth().currentUser) {
    // Retrieve JWT to identify the user to the Identity Platform service.
    // Returns the current token if it has not expired. Otherwise, this will
    // refresh the token and return a new one.
    try {
      const token = await firebase.auth().currentUser.getIdToken();
      const response = await fetch('/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          Authorization: `Bearer ${token}`,
        },
        body: 'team=' + team, // send application data (vote)
      });
      if (response.ok) {
        const text = await response.text();
        window.alert(text);
        window.location.reload();
      }
    } catch (err) {
      console.log(`Error when submitting vote: ${err}`);
      window.alert('Something went wrong... Please try again!');
    }
  } else {
    window.alert('User not signed in.');
  }
}
// [END run_end_user_token]
// [END cloudrun_end_user_token]
