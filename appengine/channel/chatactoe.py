#!/usr/bin/python2.4
#
# Copyright 2010 Google Inc. All Rights Reserved.

# pylint: disable-msg=C6310

"""Channel Tic Tac Toe

This module demonstrates the App Engine Channel API by implementing a
simple tic-tac-toe game.
"""

import datetime
import logging
import os
import random
import re
from django.utils import simplejson
from google.appengine.api import channel
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

# specify the name of your settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class Game(db.Model):
  """All the data we store for a game"""
  userX = db.UserProperty()
  userO = db.UserProperty()
  board = db.StringProperty()
  moveX = db.BooleanProperty()
  winner = db.StringProperty()
  winning_board = db.StringProperty()
  

class Wins():
  x_win_patterns = ['XXX......',
                    '...XXX...',
                    '......XXX',
                    'X..X..X..',
                    '.X..X..X.',
                    '..X..X..X',
                    'X...X...X',
                    '..X.X.X..']

  o_win_patterns = map(lambda s: s.replace('X','O'), x_win_patterns)
  
  x_wins = map(lambda s: re.compile(s), x_win_patterns)
  o_wins = map(lambda s: re.compile(s), o_win_patterns)


class GameUpdater():
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
    return simplejson.dumps(gameUpdate)

  def send_update(self):
    message = self.get_game_message()
    channel.send_message(self.game.userX.user_id() + self.game.key().id_or_name(), message)
    if self.game.userO:
      channel.send_message(self.game.userO.user_id() + self.game.key().id_or_name(), message)

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
    if position >= 0 and user == self.game.userX or user == self.game.userO:
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


class GameFromRequest():
  game = None;

  def __init__(self, request):
    user = users.get_current_user()
    game_key = request.get('g')
    if user and game_key:
      self.game = Game.get_by_key_name(game_key)

  def get_game(self):
    return self.game


class MovePage(webapp.RequestHandler):

  def post(self):
    game = GameFromRequest(self.request).get_game()
    user = users.get_current_user()
    if game and user:
      id = int(self.request.get('i'))
      GameUpdater(game).make_move(id, user)


class OpenedPage(webapp.RequestHandler):
  def post(self):
    game = GameFromRequest(self.request).get_game()
    GameUpdater(game).send_update()


class MainPage(webapp.RequestHandler):
  """The main UI page, renders the 'index.html' template."""

  def get(self):
    """Renders the main page. When this page is shown, we create a new
    channel to push asynchronous updates to the client."""
    print 'in main page get'
    user = users.get_current_user()
    game_key = self.request.get('g')
    game = None
    if user:
      if not game_key:
        game_key = user.user_id()
        game = Game(key_name = game_key,
                    userX = user,
                    moveX = True,
                    board = '         ')
        game.put()
      else:
        game = Game.get_by_key_name(game_key)
        if not game.userO:
          game.userO = user
          game.put()

      game_link = 'http://localhost:8080/?g=' + game_key

      if game:
        token = channel.create_channel(user.user_id() + game_key)
        template_values = {'token': token,
                           'me': user.user_id(),
                           'game_key': game_key,
                           'game_link': game_link,
                           'initial_message': GameUpdater(game).get_game_message()
                          }
        path = os.path.join(os.path.dirname(__file__), 'index.html')

        self.response.out.write(template.render(path, template_values))
      else:
        self.response.out.write('No such game')
    else:
      self.redirect(users.create_login_url(self.request.uri))


application = webapp.WSGIApplication([
    ('/', MainPage),
    ('/opened', OpenedPage),
    ('/move', MovePage)], debug=True)


def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
