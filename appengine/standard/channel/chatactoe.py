# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Channel Tic Tac Toe
This module demonstrates the App Engine Channel API by implementing a
simple tic-tac-toe game.
For more information, see the README.md.
"""

# [START all]
import json
import os
import re

from google.appengine.api import app_identity
from google.appengine.api import channel
from google.appengine.api import users
from google.appengine.ext import db
import jinja2
import webapp2

CLOUD_PROJECT_ID = app_identity.get_application_id()


class Game(db.Model):
    """All the data we store for a game"""
    userX = db.UserProperty()
    userO = db.UserProperty()
    board = db.StringProperty()
    moveX = db.BooleanProperty()
    winner = db.StringProperty()
    winning_board = db.StringProperty()


class Wins():
    x_win_patterns = ['XXX......', '...XXX...', '......XXX', 'X..X..X..',
                      '.X..X..X.', '..X..X..X', 'X...X...X', '..X.X.X..']

    o_win_patterns = map(lambda s: s.replace('X', 'O'), x_win_patterns)

    x_wins = map(lambda s: re.compile(s), x_win_patterns)
    o_wins = map(lambda s: re.compile(s), o_win_patterns)


# [START validate_message_3]
class GameUpdater():
    """Creates an object to store the game's state, and handles validating moves
  and broadcasting updates to the game."""
    game = None

    def __init__(self, game):
        self.game = game

    def get_game_message(self):
        gameUpdate = {
            'board': self.game.board,
            'userX': self.game.userX.user_id(),
            'userO': '' if not self.game.userO else self.game.userO.user_id(),
            'moveX': self.game.moveX,
            'winner': self.game.winner,
            'winningBoard': self.game.winning_board
        }
        return json.dumps(gameUpdate)

    def send_update(self):
        message = self.get_game_message()
        channel.send_message(
            self.game.userX.user_id() + self.game.key().id_or_name(), message)
        if self.game.userO:
            channel.send_message(self.game.userO.user_id() +
                                 self.game.key().id_or_name(), message)

    def check_win(self):
        if self.game.moveX:
            # O just moved, check for O wins
            wins = Wins().o_wins
            potential_winner = self.game.userO.user_id()
        else:
            # X just moved, check for X wins
            wins = Wins().x_wins
            potential_winner = self.game.userX.user_id()

        for win in wins:
            if win.match(self.game.board):
                self.game.winner = potential_winner
                self.game.winning_board = win.pattern
                return

    def make_move(self, position, user):
        if (position >= 0 and user == self.game.userX or
                user == self.game.userO):
            if self.game.moveX == (user == self.game.userX):
                boardList = list(self.game.board)
                if (boardList[position] == ' '):
                    boardList[position] = 'X' if self.game.moveX else 'O'
                    self.game.board = "".join(boardList)
                    self.game.moveX = not self.game.moveX
                    self.check_win()
                    self.game.put()
                    self.send_update()
                    return
# [END validate_message_3]


# [START validate_message_2]
class GameFromRequest():
    game = None

    def __init__(self, request):
        user = users.get_current_user()
        game_key = request.get('g')
        if user and game_key:
            self.game = Game.get_by_key_name(game_key)

    def get_game(self):
        return self.game
# [END validate_message_2]


# [START validate_message_1]
class MovePage(webapp2.RequestHandler):
    def post(self):
        game = GameFromRequest(self.request).get_game()
        user = users.get_current_user()
        if game and user:
            id = int(self.request.get('i'))
            GameUpdater(game).make_move(id, user)
# [END validate_message_1]


class OpenedPage(webapp2.RequestHandler):
    def post(self):
        game = GameFromRequest(self.request).get_game()
        GameUpdater(game).send_update()


# [START create_channel_1]
class MainPage(webapp2.RequestHandler):
    """The main UI page, renders the 'index.html' template."""

    def get(self):
        """Renders the main page. When this page is shown, we create a new
    channel to push asynchronous updates to the client."""
        user = users.get_current_user()
        game_key = self.request.get('g')
        game = None
        if user:
            if not game_key:
                game_key = user.user_id()
                game = Game(key_name=game_key,
                            userX=user,
                            moveX=True,
                            board='         ')
                game.put()
            else:
                game = Game.get_by_key_name(game_key)
                # if not game.userO:
                if not game.userO and game.userX != user:
                    game.userO = user
                    game.put()

            global CLOUD_PROJECT_ID
            game_link = (
                'https://' + CLOUD_PROJECT_ID + '.appspot.com/?g=' + game_key)

            if game:
                token = channel.create_channel(user.user_id() + game_key)
                template_values = {'token': token,
                                   'me': user.user_id(),
                                   'game_key': game_key,
                                   'game_link': game_link,
                                   'initial_message':
                                   GameUpdater(game).get_game_message()}
                template = jinja_environment.get_template('index.html')
                self.response.out.write(template.render(template_values))
            else:
                self.response.out.write('No such game')
        else:
            self.redirect(users.create_login_url(self.request.uri))
# [END create_channel_1]


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/opened', OpenedPage),
    ('/move', MovePage)
], debug=True)

# [END all]
