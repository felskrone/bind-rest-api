#!/usr/bin/env bash
/etc/init.d/bind9 start
watchmedo auto-restart -d "/app" --recursive -p "*.py;*.txt;*.yaml" python3 app.py
