FROM alpine:3.14

LABEL org.opencontainers.image.authors "Richard Kojedzinszky <richard@kojedz.in>"
LABEL org.opencontainers.image.source https://github.com/rkojedzinszky/docker-registry-auth

ENV APP_USER=docker-registry-auth \
    APP_HOME=/opt/docker-registry-auth

RUN apk add --no-cache python3 py3-pip openssl supervisor nginx py3-psycopg2 uwsgi-python3 \
        py3-cryptography && \
	mkdir -p /data $APP_HOME && \
	adduser -u 17490 -D -H -h $APP_HOME $APP_USER && \
	chown -R $APP_USER /var/lib/nginx /var/log/nginx

WORKDIR $APP_HOME

COPY dra dra
COPY manage.py manage.py
COPY requirements.txt requirements.txt

RUN	pip3 install -r requirements.txt && \
	python3 manage.py collectstatic --no-input && \
	rm -rf /root/.cache && \
	ln -sf /data/local_settings.py

ADD docker-assets/ /

EXPOSE 8080

ENV UWSGI_THREADS 4

USER 17490

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
