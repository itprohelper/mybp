# A MySQL container.
FROM mysql:5.7
LABEL maintainer="ITPro Helper"

ENV MYSQL_DATABASE mbp

COPY ./mysql/ /docker-entrypoint-initdb.d/

EXPOSE 3306
CMD ["mysqld"]
