FROM postgres

RUN localedef -i ru_RU -c -f UTF-8 -A /usr/share/locale/locale.alias ru_RU.UTF-8

ENV LANG ru_RU.utf8

ENV POSTGRES_USER root

ENV POSTGRES_PASSWORD artem

COPY init.sql /docker-entrypoint-initdb.d/