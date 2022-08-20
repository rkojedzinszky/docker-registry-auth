#!/bin/sh

python3 manage.py migrate

cd /tmp

exec "$@"
