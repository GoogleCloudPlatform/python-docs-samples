#!/bin/bash

# EXIT CODES - ERROR
E_OPTERROR=85

# ANSI Sequences
ANSI_RESET="\033[0m"

# Effects
ANSI_NORMAL=0
ANSI_BOLD=1
ANSI_UNDER=4
ANSI_BLINK=5
ANSI_REVERSE=7
ANSI_INVISIBLE=8
# Foreground Colors
ANSI_F_BLACK="30"
ANSI_F_RED="31"
ANSI_F_GREEN="32"
ANSI_F_BROWN="33"
ANSI_F_BLUE="34"
ANSI_F_PURPLE="35"
ANSI_F_CYAN="36"
ANSI_F_LIGHT_GRAY="37"
# Background Colors
ANSI_B_BLACK="40"
ANSI_B_RED="41"
ANSI_B_GREEN="42"
ANSI_B_YELLOW="43"
ANSI_B_BLUE="44"
ANSI_B_MAGENTA="45"
ANSI_B_CYAN="46"
ANSI_B_WHITE="47"

# internal functions to help output formatting

ansi_print() {
  printf "\033[$1"
  shift
  while [ "$#" -gt "1" ]; do
    printf ";$1"
    shift
  done
  printf "m$1$ANSI_RESET"
}

ansi_println() {
  ansi_print "$@"
  printf "\n"
}

_log_date() {
  printf "[`date "+%Y-%m-%d %H:%M:%S"`] "
}

_info() {
  _log_date
  ansi_print $ANSI_REVERSE $ANSI_F_GREEN "INFO"
  echo "$@"
}

_error() {
  _log_date
  ansi_print $ANSI_REVERSE $ANSI_F_RED "ERROR"
  echo "$@" >&2
}

_warn() {
  _log_date
  ansi_print $ANSI_REVERSE $ANSI_F_BROWN "WARN"
  echo "$@" >&2
}

# public functions to print messages

err() {
  _error " $@"
}

log() {
  _info " $@"
}

# helper functions to change text case

to_lower() {
  local text=$1
  echo $text|tr '[:upper:]' '[:lower:]'
}

to_upper() {
  local text=$1
  echo $text|tr '[:lower:]' '[:upper:]'
}

# public functions to print and execute commands

run_command(){
  log "executing $@"
  "$@"
}

sim_command(){
  log "simulate $@"
}
