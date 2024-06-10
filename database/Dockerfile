FROM mariadb:11.5.1-rc

RUN chown -R mysql:root /var/lib/mysql/
COPY init.sql /docker-entrypoint-initdb.d/init.sql

EXPOSE 3306
