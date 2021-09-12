#!/bin/sh

RSA_KEY=${RSA_KEY:-/data/key.pem}

umask 077

if [ ! -f "${RSA_KEY}" ]; then
	openssl genrsa -out "${RSA_KEY}" 4096
fi

python3 manage.py migrate

cd /tmp

exec "$@"
