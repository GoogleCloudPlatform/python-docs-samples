// Copyright 2016, Google, Inc.
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

$(function(){
  // This is the host for the backend.
  // TODO: When running Firenotes locally, set to http://localhost:8081. Before
  // deploying the application to a live production environment, change to
  // https://backend-dot-<PROJECT_ID>.appspot.com as specified in the
  // backend's app.yaml file.
  var backendHostUrl = '<your-backend-url>';

  // Initialize Firebase
  // TODO: Replace with your project's customized code snippet
  var config = {
    apiKey: "<API_KEY>",
    authDomain: "<PROJECT_ID>.firebaseapp.com",
    databaseURL: "https://<DATABASE_NAME>.firebaseio.com",
    storageBucket: "<BUCKET>.appspot.com",
  };

  // This is passed into the backend to authenticate the user.
  var userIdToken = null;

  // Firebase log-in
  function configureFirebaseLogin() {

    firebase.initializeApp(config);

    // [START onAuthStateChanged]
    firebase.auth().onAuthStateChanged(function(user) {
      if (user) {
        $('#logged-out').hide();
        var name = user.displayName;

        /* If the provider gives a display name, use the name for the
        personal welcome message. Otherwise, use the user's email. */
        var welcomeName = name ? name : user.email;

        user.getToken().then(function(idToken) {
          userIdToken = idToken;

          /* Now that the user is authenicated, fetch the notes. */
          fetchNotes();

          $('#user').text(welcomeName);
          $('#logged-in').show();

        });

      } else {
        $('#logged-in').hide();
        $('#logged-out').show();

      }
    // [END onAuthStateChanged]

    });

  }

  // [START configureFirebaseLoginWidget]
  // Firebase log-in widget
  function configureFirebaseLoginWidget() {
    var uiConfig = {
      'signInSuccessUrl': '/',
      'signInOptions': [
        // Leave the lines as is for the providers you want to offer your users.
        firebase.auth.GoogleAuthProvider.PROVIDER_ID,
        firebase.auth.FacebookAuthProvider.PROVIDER_ID,
        firebase.auth.TwitterAuthProvider.PROVIDER_ID,
        firebase.auth.GithubAuthProvider.PROVIDER_ID,
        firebase.auth.EmailAuthProvider.PROVIDER_ID
      ],
      // Terms of service url
      'tosUrl': '<your-tos-url>',
    };

    var ui = new firebaseui.auth.AuthUI(firebase.auth());
    ui.start('#firebaseui-auth-container', uiConfig);
  }
  // [END configureFirebaseLoginWidget]

  // [START fetchNotes]
  // Fetch notes from the backend.
  function fetchNotes() {
    $.ajax(backendHostUrl + '/notes', {
      /* Set header for the XMLHttpRequest to get data from the web server
      associated with userIdToken */
      headers: {
        'Authorization': 'Bearer ' + userIdToken
      }
    }).then(function(data){
      $('#notes-container').empty();
      // Iterate over user data to display user's notes from database.
      data.forEach(function(note){
        $('#notes-container').append($('<p>').text(note.message));
      });
    });
  }
  // [END fetchNotes]

  // [START signOutBtn]
  // Sign out a user
  var signOutBtn =$('#sign-out');
  signOutBtn.click(function(event) {
    event.preventDefault();

    firebase.auth().signOut().then(function() {
      console.log("Sign out successful");
    }, function(error) {
      console.log(error);
    });
  });
  // [END signOutBtn]

  // [START saveNoteBtn]
  // Save a note to the backend
  var saveNoteBtn = $('#add-note');
  saveNoteBtn.click(function(event) {
    event.preventDefault();

    var noteField = $('#note-content');
    var note = noteField.val();
    noteField.val("");

    /* Send note data to backend, storing in database with existing data
    associated with userIdToken */
    $.ajax(backendHostUrl + '/notes', {
      headers: {
        'Authorization': 'Bearer ' + userIdToken
      },
      method: 'POST',
      data: JSON.stringify({'message': note}),
      contentType : 'application/json'
    }).then(function(){
      // Refresh notebook display.
      fetchNotes();
    });

  });
  // [END saveNoteBtn]

  configureFirebaseLogin();
  configureFirebaseLoginWidget();

});
