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
import urllib
import json as simplejson
from google.appengine.api import channel
from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import jwt  # Requires: pip install python-jwt
import Crypto.PublicKey.RSA as RSA  # Requires: pip install pycrypto

# Firebase database url/channels#
fire_url = 'https://imposing-mind-131903.firebaseio.com/channels/'
# Firebase database server authorization key #
# This is used to authenticate the server and authorize write access
firebase_secret = '1O9VkxnyjEvbRIx1dLohPDZmhxqDjJgsPqikHwW7'
# Get your service account's email address and private key from the JSON key file
service_account_email = "imposing-mind-131903@appspot.gserviceaccount.com"
# private_key = RSA.importKey("-----BEGIN PRIVATE KEY-----\n...")
# NOTE: NEVER put secret credentials in code. This is done in this example solely
# for convenience purposes. Best practice is to keep this information in a
# separate file that can be referenced by your code
private_key = RSA.importKey("-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCh360T6TwZHQVE\nwWxABahw0pFc+331Kq9b7AdkfCcCpoFOTPkJR1a6sOKS+Veb7G5eJUg6k7/8BJ/Z\ntQwyf/1UPo8SvsixYprOuH9MO34Wqh9O1vpq0lBy6FX7Bxq5jlbJOrVgJBgNWBnv\nMRnphQhRHQmpzA9mLEfToqHzfCJP91DGJYRGcuEEH/0QOgc8Lkvmyc7dBgNxakS9\nwGvSJ+aZ/7+HYyEo2oVpFkj1rvVJf6FxcXoqep6UuK/BpeQ2HbB+gLvEaWSLtgT3\ncR4imuN6sGPYjOqc+PC/optegiI/1gdcRyVEDR6B+LwWkpjq+ciXFlPLHLvMuW0R\nIL1wLnMtAgMBAAECggEBAJ3UldFALFTgMu7jGUUjPyUiapGatSmCwRCDhoG3e+Hd\nr15FNtyRLkNBjOl5LK7fTI2HFHHo9dwoNiPznzzuBndJt/6y/sPWPNMqmRQfPcWj\ngntAqVHWVpJzbsIgHzKlUoFKOObQypLYQBE0cut5xq4v/egNC0a4DiCQBhB+DIai\nNI3k3Zu1/CxfBuzFZOFlu77m/xV3TiYbRwHkHDOAVqY7XaFdnmSD9XsAgDGJAaPA\nDYl5Zqey1qjn+PtBFbA2JxvrJS75PrvFq8DRq7p1dX0mQ6priIJIo4DEWgZVe7EH\nCXYNAFLKuPL2UphOdDTlIwjsUIrgaCh5oVNBwxedcxECgYEA0IGWd7nygeQ2hGJR\nybhYy+7T7xzrwIqrSQWXL5fahGUp2J/x5IDMk3+Iyk8g43O5UgQEeYZBLdcjsrti\nob83WS2G1LN2VtoH5zsB1tzn12uh2lT2+10JhOVW8fCPGsQrFF2ynZKkY2QOjEW3\nT4LeNBl25+vriDL5+qAlHgospSMCgYEAxr7bL5v7t35JYlNAlGhXL5m45AsS/M1b\nTZYs7b0Ys2ECLgEV3PZgHQYZ9Rl7UtyUGUG2t5hP0WN6ihysaYMkvsw3OdvtylpP\nXKwlxPTEqKk8E7orkIzuUw5s81/RNVIWf9FxnjWB4BBYMUN6v/ZnmmVMoVGPINDR\nmKAdvx9d028CgYEAlKiwJTC4jI+vpveKpK4A8XWYOVV/aMn1kZygzFgSfm66RS7U\ngjyqn0dAui1sn3601Jr0rchg1FQdqaMckYIJ7lUdWq2RZB8Tn3NcvlrGGbstrMMD\nTPhqfwwcz2baQRU4Oc8MOHiDKDIAhVZ3egMudirpsjVsurDNtjlT/XT3m80CgYEA\nlpEtGOqBTshb7CPKPyS1OJirHAjPv7oMO8FUFGA4AF2z+wpTd+0nb5WZwLgnV+VI\nRcIlHP5FKgrFYTDL5bu28N1h0XGuuqikiz7X9ljBTE259/AI5R//xeid3dtvcYfZ\nB8iy3PsIg6meRuQqcJfKcYvg/C3/0wqgX5KeNpcay/0CgYAxm3iYvUKDh/az5JNA\nATgnxTDDaZASaIjYLfdctqMDb90vIyQvq+JlKD85F3jy8Z5mlbDIxEzM7MkJn1yR\nJB7kB+dUxVLbuuzFMggbbURylVgtMzmddub7LfN8nAQ8EV8Fp4oYdDhcioPI6Qhi\n81se59mK/q33B7iX8GvyPf/pIQ==\n-----END PRIVATE KEY-----\n")

# This method is used to create secure custom tokens to be passed to clients
# it takes a unique id (uid) that will be used by Firebase's security rules
# to prevent unauthorized access. In this case, the uid will be the channel id
# which is a combination of user_id and game_key
def create_custom_token(uid):
  try:
    payload = {
      "iss": service_account_email,
      "sub": service_account_email,
      "aud": "https://identitytoolkit.googleapis.com/google.identity.identitytoolkit.v1.IdentityToolkit",
      "uid": uid
    }
    exp = datetime.timedelta(minutes=60)
    return jwt.generate_jwt(payload, private_key, "RS256", exp)
  except Exception as e:
    print "Error creating custom token: " + e.message
    return None

# auth token for the server
gae_auth_token = firebase_secret # gives the server full write access to Firebase


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
    # send updated game state to user X
    FireChannel(fire_url).send_message(	u_id=self.game.userX.user_id() + self.game.key().id_or_name(), 
    									message=message,
    									is_delete=False)
    # send updated game state to user O
    if self.game.userO:
    	FireChannel(fire_url).send_message(	u_id=self.game.userO.user_id() + self.game.key().id_or_name(), 
    									message=message,
    									is_delete=False)

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

class DeletePage(webapp.RequestHandler):

  def post(self):
    game = GameFromRequest(self.request).get_game()
    user = users.get_current_user()
    if game and user:
      FireChannel(fire_url).send_message(u_id=user.user_id() + game.key().id_or_name(), 
    									message=None,
    									is_delete=True)

class OpenedPage(webapp.RequestHandler):
  def post(self):
    game = GameFromRequest(self.request).get_game()
    GameUpdater(game).send_update()

# This class has a set of helper functions on top of url fetch to make it easier
# to send commands to Firebase. It consists of a constructor that saves the
# Firebase database URL. In addition, it implements send_message, which updates
# a path on Firebase based on the unique identifier u_id. In this example
# u_id == channel_id == user_id + game_key
class FireChannel():
	base_url = None

	def __init__(self, base_url):
		self.base_url = base_url

	def send_message(self, u_id, message, is_delete):
		try:
			headers = {'Content-Type': 'application/x-www-form-urlencoded'}
			method_type = None
			if (is_delete): 
				method_type = urlfetch.DELETE 
			else: 
				method_type = urlfetch.PATCH
			# always using patch in this example for writes
			# because it updates or creates but never overwrites
			result = urlfetch.fetch(
        		url=self.base_url + u_id + '.json?auth=' + gae_auth_token, # create a new stream using unique id and server auth key
        		payload=message,
        		method=method_type,
        		headers=headers,
        		validate_certificate=True)
			json_data = simplejson.loads(result.content)
			logging.info(json_data.get("message"))
			return result.content
		except urlfetch.Error:
			logging.exception('Caught exception fetching url')



class MainPage(webapp.RequestHandler):
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
        # choose a unique identifier for channel_id
        channel_id = user.user_id() + game_key
        # encrypt the channel_id and send it as a custom token to the client
        # Firebase's data security rules will be able to decrypt the token
        # and prevent unauthorized access
        client_auth_token = create_custom_token(channel_id)
        output = FireChannel(fire_url).send_message(	u_id=channel_id,
        							message=GameUpdater(game).get_game_message(),
        							is_delete=False)

        # push all the data to the html template so the client will have access
        template_values = {'token': client_auth_token,
        				   'channel_id': channel_id,
                           'me': user.user_id(),
                           'game_key': game_key,
                           'game_link': game_link,
                           'initial_message': urllib.unquote(GameUpdater(game).get_game_message())
                          }
        path = os.path.join(os.path.dirname(__file__), 'fire_index.html')

        self.response.out.write(template.render(path, template_values))
      else:
        self.response.out.write('No such game')
    else:
      self.redirect(users.create_login_url(self.request.uri))


application = webapp.WSGIApplication([
    ('/', MainPage),
    ('/opened', OpenedPage),
    ('/delete', DeletePage),
    ('/move', MovePage)], debug=True)


def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
