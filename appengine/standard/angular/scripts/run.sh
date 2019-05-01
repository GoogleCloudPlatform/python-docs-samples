#!/bin/bash
#
set -uex

dev_appserver.py \
  --host 0.0.0.0 \
  --admin_host 127.0.0.1 \
  --skip_sdk_update_check yes \
  . $*
