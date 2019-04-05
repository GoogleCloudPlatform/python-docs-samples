#!/usr/bin/env python3
#pylint: disable=missing-docstring, C0301


BLUE = '\033[94m'
GREEN = '\033[92m'
WHITE = '\033[37m'
YELLOW = '\033[93m'
SOLARIZED = '\033[33m'
RED = '\033[91m'
ENDC = '\033[0m'


def print_in_color(color, msg):
    print('{}{}{}'.format(color, msg, ENDC))


def step(msg):
    print('\n{}==> {}{}{}'.format(GREEN, WHITE, msg, ENDC))


def info(msg):
    print('{}  -> {}{}{}'.format(BLUE, WHITE, msg, ENDC))


def warn(msg):
    print('{}  -> {}{}{}'.format(YELLOW, WHITE, msg, ENDC))


def error(msg):
    print('{}==> ERROR: {}{}'.format(RED, msg, ENDC))
