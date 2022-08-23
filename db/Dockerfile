# A MariaDB container.
FROM mariadb:10.5
LABEL maintainer="ITPro Helper"

RUN apt update && apt install -y python3

# No ve el resto de los files para correr flask
#ADD createdb.py /

ENV MYSQL_DATABASE bp

# Create MySQL tables using createtable.sql script inside mysql folder.
# Todo: Have SLQAlchemy create the tables using models.py
# COPY ./mysql/ /docker-entrypoint-initdb.d/

EXPOSE 3306
CMD ["mysqld"]
