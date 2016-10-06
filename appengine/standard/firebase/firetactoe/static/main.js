/**
 * Copyright 2016 Google Inc. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

'use strict';

/**
 * @fileoverview Tic-Tac-Toe, using the Firebase API
 */

/**
 * @param gameKey - a unique key for this game.
 * @param me - my user id.
 * @param token - secure token passed from the server
 * @param channelId - id of the 'channel' we'll be listening to
 */
function initGame(gameKey, me, token, channelId, initialMessage) {
  var state = {
    gameKey: gameKey,
    me: me
  };

  // This is our Firebase realtime DB path that we'll listen to for updates
  // We'll initialize this later in openChannel()
  var channel = null;

  /**
   * Updates the displayed game board.
   */
  function updateGame() {
    for (var i = 0; i < 9; i++) {
      var square = document.getElementById(i);
      square.innerHTML = state.board[i];
      if (state.winner && state.winningBoard) {
        if (state.winningBoard[i] === state.board[i]) {
          if (state.winner === state.me) {
            square.style.background = 'green';
          } else {
            square.style.background = 'red';
          }
        } else {
          square.style.background = 'white';
        }
      }
    }

    var display = {
      'other-player': 'none',
      'your-move': 'none',
      'their-move': 'none',
      'you-won': 'none',
      'you-lost': 'none',
      'board': 'block',
      'this-game': 'block',
    };

    if (!state.userO) {
      display['other-player'] = 'block';
      display['board'] = 'none';
      display['this-game'] = 'none';
    } else if (state.winner === state.me) {
      display['you-won'] = 'block';
    } else if (state.winner) {
      display['you-lost'] = 'block';
    } else if (isMyMove()) {
      display['your-move'] = 'block';
    } else {
      display['their-move'] = 'block';
    }

    for (var label in display) {
      document.getElementById(label).style.display = display[label];
    }
  }

  function isMyMove() {
    return !state.winner && (state.moveX === (state.userX === state.me));
  }

  function myPiece() {
    return state.userX === state.me ? 'X' : 'O';
  }

  /**
   * This message sends POST requests back to the App Engine server
   */
  function sendMessage(path, optParam) {
    path += '?g=' + state.gameKey;
    if (optParam) {
      path += '&' + optParam;
    }
    var xhr = new XMLHttpRequest();
    xhr.open('POST', path, true);
    xhr.send();
  }

  /**
   * Send the user's latest move back to the server
   */
  function moveInSquare(e) {
    var target = e.target || e.srcElement;
    var id = parseInt(target.id, 10);
    if (isMyMove() && state.board[id] === ' ') {
      sendMessage('/move', 'i=' + id);
    }
  }

  function highlightSquare(e) {
    if (state.winner) {
      return;
    }
    var target = e.target || e.srcElement;
    var id = parseInt(target.id, 10);
    for (var i = 0; i < 9; i++) {
      var color;
      if (i === id  && isMyMove()) {
        if (state.board[i] === ' ') {
          color = 'lightBlue';
        } else {
          color = 'lightGrey';
        }
      } else {
        color = 'white';
      }

      document.getElementById(i).style['background'] = color;
    }
  }

  /**
   * This method lets the server know that the user has opened the channel
   * After this method is called, the server may begin to send updates
   */
  function onOpened() {
    sendMessage('/opened');
  }

  /**
   * This deletes the data associated with the Firebase path
   * it is critical that this data be deleted since it costs money
   */
  function deleteChannel() {
    sendMessage('/delete');
  }

  /**
   * This method is called every time an event is fired from Firebase
   * it updates the entire game state and checks for a winner
   * if a player has won the game, this function calls the server to delete
   * the data stored in Firebase
   */
  function onMessage(m) {
    var newState = m;
    for (var key in newState) {
      state[key] = newState[key];
    }
    updateGame();
    // now check to see if there is a winner
    if (channel && state.winner && state.winningBoard) {
      channel.off(); //stop listening on this path
      deleteChannel(); //delete the data we wrote
    }
  }

  /**
   * This function opens a realtime communication channel with Firebase
   * It logs in securely using the client token passed from the server
   * then it sets up a listener on the proper database path (also passed by server)
   * finally, it calls onOpened() to let the server know it is ready to receive messages
   */
  function openChannel() {
    // sign into Firebase with the token passed from the server
    firebase.auth().signInWithCustomToken(token).catch(function(error) {
      console.log('Login Failed!', error.code);
      console.log('Error message: ', error.message);
    });

    // setup a database reference at path /channels/channelId
    channel = firebase.database().ref('channels/' + channelId);
    // add a listener to the path that fires any time the value of the data changes
    channel.on('value', function(data) {
      onMessage(data.val());
    });
    onOpened();
    // let the server know that the channel is open
  }

  /**
   * This function opens a communication channel with the server
   * then it adds listeners to all the squares on the board
   * next it pulls down the initial game state from template values
   * finally it updates the game state with those values by calling onMessage()
   */
  function initialize() {
    openChannel();

    for (var i = 0; i < 9; i++) {
      var square = document.getElementById(i);
      square.onmouseover = highlightSquare;
      square.onclick = moveInSquare;
    }

    onMessage(initialMessage);
  }

  setTimeout(initialize, 100);
}
