# A MySQL container.
FROM mysql:5.7
LABEL maintainer="ITPro Helper"

ENV MYSQL_DATABASE mbp

# Create MySQL tables using createtable.sql script inside mysql folder.
# Todo: Have SLQAlchemy create the tables using models.py
# COPY ./mysql/ /docker-entrypoint-initdb.d/

EXPOSE 3306
CMD ["mysqld"]
